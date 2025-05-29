# main.py

import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk     # pip install pillow
import pandas as pd

# ——— Importa tus módulos existentes ———
from gestor_datos import cargar_vuelos, cargar_usuarios, cargar_reservas, guardar_reservas
from logica import login, consultar_disponibilidad, crear_reserva, simular_pago, generar_boleto
from algoritmos import asignar_asiento_greedy

# ——— Variables “globales” ———
root = None
usuario_actual = None
vuelos = []
usuarios = []
reservas = []
reserva_en_proceso = None
_fondo_img = None

def cargar_todos_los_datos():
    global vuelos, usuarios, reservas
    df_v = cargar_vuelos()
    vuelos = df_v.to_dict('records') if not df_v.empty else []
    df_u = cargar_usuarios()
    usuarios = df_u.to_dict('records') if not df_u.empty else []
    df_r = cargar_reservas()
    reservas = df_r.to_dict('records') if not df_r.empty else []

def limpiar_ventana():
    for w in root.winfo_children():
        w.destroy()

# — Pantalla de Login —
def mostrar_login():
    limpiar_ventana()
    frame = ttk.Frame(root, padding=20); frame.pack(expand=True)
    ttk.Label(frame, text="Iniciar sesión", font=('Arial',14,'bold')).pack(pady=8)
    ttk.Label(frame, text="Usuario:").pack(anchor='w')
    e_u = ttk.Entry(frame); e_u.pack(fill='x')
    ttk.Label(frame, text="Contraseña:").pack(anchor='w')
    e_c = ttk.Entry(frame, show="*"); e_c.pack(fill='x')

    def intentar():
        global usuario_actual
        user = login(usuarios, e_u.get().strip(), e_c.get().strip())
        if user:
            usuario_actual = user
            mostrar_menu_principal()
        else:
            messagebox.showerror("Error","Usuario o contraseña incorrectos.")
    ttk.Button(frame, text="Ingresar", command=intentar).pack(pady=10)

# — Menú principal —
def mostrar_menu_principal():
    limpiar_ventana()
    
    # Canvas para el fondo
    canvas = tk.Canvas(root, highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    
    # Frame para el menú (centrado)
    frame = ttk.Frame(root, style="Menu.TFrame")
    frame.place(relx=0.5, rely=0.5, anchor='center')
    
    try:
        # Cargar imagen original
        original_img = Image.open("fondoMenu.jpg")
        
        # Función para redimensionar el fondo
        def redimensionar_fondo(event=None):
            canvas_width = canvas.winfo_width()
            canvas_height = canvas.winfo_height()
            
            if canvas_width > 0 and canvas_height > 0:
                # Redimensionar SIN mantener relación de aspecto
                resized_img = original_img.resize((canvas_width, canvas_height), Image.LANCZOS)
                bg_image = ImageTk.PhotoImage(resized_img)
                
                # Guardar referencia y actualizar
                canvas.bg_image = bg_image
                canvas.delete("background")
                canvas.create_image(0, 0, image=bg_image, anchor="nw", tags="background")
        
        # Configurar eventos
        canvas.bind("<Configure>", redimensionar_fondo)
        redimensionar_fondo()  # Llamada inicial
        
    except Exception as e:
        print(f"Error cargando fondo: {e}")
        canvas.config(bg="#b0e0ff")  # Fondo alternativo

    # Contenido del menú
    ttk.Label(
        frame,
        text=f"Bienvenido/a, {usuario_actual.get('usuario','')}",
        font=('Arial',16,'bold'),
        background="#b0e0ff"
    ).pack(pady=15)

    opciones = [
        ("Consultar vuelos", consultar_vuelos),
        ("Reservar vuelo", reservar_vuelo),
        ("Pagar", pagar_reserva),
        ("Salir", root.quit)
    ]
    
    def animar(fn):
        lbl = ttk.Label(frame, text="Cargando", font=('Arial',13,'italic'), foreground="#2573b9")
        lbl.pack(pady=10)
        puntos = ["", ".", "..", "...", "...."]
        
        def paso(i=0):
            lbl.config(text="Cargando" + puntos[i])
            if i < len(puntos)-1:
                root.after(100, paso, i+1)
            else:
                lbl.config(text="¡Listo!")
                root.after(200, lambda: [lbl.destroy(), fn()])
        paso()
    
    for txt, fn in opciones:
        ttk.Button(frame, text=txt, width=25, command=lambda f=fn: animar(f)).pack(pady=6)

    style = ttk.Style()
    style.configure("Menu.TFrame", background="#b0e0ff", relief="flat")

# — Consultar vuelos —
def consultar_vuelos():
    limpiar_ventana()
    frame = ttk.Frame(root, padding=20); frame.pack(expand=True,fill='both')
    ttk.Label(frame, text="Consulta de vuelos", font=('Arial',12,'bold')).pack(pady=8)

    frm = ttk.Frame(frame); frm.pack(pady=5)
    ttk.Label(frm, text="Origen:").grid(row=0,column=0)
    e_or = ttk.Entry(frm,width=10); e_or.grid(row=0,column=1,padx=4)
    ttk.Label(frm, text="Destino:").grid(row=0,column=2)
    e_de = ttk.Entry(frm,width=10); e_de.grid(row=0,column=3,padx=4)
    ttk.Label(frm, text="Fecha (YYYY-MM-DD):").grid(row=0,column=4)
    e_fe = ttk.Entry(frm,width=12); e_fe.grid(row=0,column=5,padx=4)

    cols = ("origen","destino","fecha","hora","precio")
    tree = ttk.Treeview(frame, columns=cols, show='headings', height=8)
    for c in cols:
        tree.heading(c, text=c.capitalize())
        tree.column(c, width=90, anchor='center')
    tree.pack(fill='both',expand=True,pady=8)

    def buscar():
        o,d,f = e_or.get().strip(), e_de.get().strip(), e_fe.get().strip()
        if not (o and d and f):
            messagebox.showwarning("Faltan campos","Ingresa origen, destino y fecha")
            return
        res = consultar_disponibilidad(vuelos, o, d, f)
        for i in tree.get_children(): tree.delete(i)
        if not res:
            messagebox.showinfo("Sin resultados","No se encontraron vuelos.")
        for v in res:
            fv, hv = v['fecha'][:10], v['fecha'][11:16]
            tree.insert('', 'end', values=(v['origen'],v['destino'],fv,hv,f"${v['precio']:.2f}"))

    ttk.Button(frm, text="Buscar", command=buscar).grid(row=0,column=6,padx=4)
    ttk.Button(frame, text="Volver", command=mostrar_menu_principal).pack(pady=6)

# — Reservar vuelo —
def reservar_vuelo():
    global reservas, reserva_en_proceso
    limpiar_ventana()
    frame = ttk.Frame(root, padding=20); frame.pack(expand=True,fill='both')
    ttk.Label(frame, text="Reservar vuelo", font=('Arial',12,'bold')).pack(pady=8)

    ttk.Label(frame, text="Seleccione vuelo:").pack()
    combo_v = ttk.Combobox(frame, width=60, state="readonly")
    combo_v['values'] = [f"{v['origen']}→{v['destino']}|{v['fecha']}|${v['precio']:.2f}" for v in vuelos]
    combo_v.pack()

    ttk.Label(frame, text="Seleccione asiento:").pack(pady=4)
    combo_a = ttk.Combobox(frame, width=20, state="readonly"); combo_a.pack()

    def upd(evt=None):
        i = combo_v.current()
        if i<0:
            combo_a['values'] = []; return
        a_list = vuelos[i].get('asientos_disponibles',[])
        combo_a['values'] = (["No hay asientos"] if not a_list
                             else [f"{a['codigo']} (${a['precio']:.2f})" for a in a_list])
        if a_list: combo_a.current(0)
    combo_v.bind("<<ComboboxSelected>>", upd)

    def on_res():
        iv, ia = combo_v.current(), combo_a.current()
        if iv<0 or ia<0:
            messagebox.showwarning("Seleccione","Elige vuelo y asiento"); return
        sel = vuelos[iv].get('asientos_disponibles',[])
        if not sel:
            messagebox.showerror("Sin asientos","Este vuelo no tiene asientos"); return
        cod = sel[ia]['codigo']
        r = crear_reserva(usuario_actual, vuelos[iv], cod)
        reserva_en_proceso = r; reservas.append(r)
        guardar_reservas(pd.DataFrame(reservas))
        messagebox.showinfo("¡Listo!","Reserva creada. Procede al pago.")
        mostrar_menu_principal()

    ttk.Button(frame, text="Reservar", command=on_res).pack(pady=8)
    ttk.Button(frame, text="Volver", command=mostrar_menu_principal).pack()

# — Pagar reserva —
def pagar_reserva():
    global reserva_en_proceso
    limpiar_ventana()
    frame = ttk.Frame(root, padding=20); frame.pack(expand=True)
    ttk.Label(frame, text="Pago de reserva", font=('Arial',12,'bold')).pack(pady=8)

    if not reserva_en_proceso:
        ttk.Label(frame, text="No hay reserva pendiente.").pack(pady=6)
        ttk.Button(frame, text="Volver", command=mostrar_menu_principal).pack()
        return

    inf = reserva_en_proceso
    ttk.Label(frame, text=f"Reserva: {inf['id_reserva']}  Monto: ${inf['precio']:.2f}").pack(pady=5)
    ttk.Label(frame, text="Número de tarjeta:").pack(anchor='w'); e_num = ttk.Entry(frame); e_num.pack(fill='x')
    ttk.Label(frame, text="CVV:").pack(anchor='w');             e_cvv = ttk.Entry(frame,width=5); e_cvv.pack()
    ttk.Label(frame, text="Vencimiento (MM/YY):").pack(anchor='w'); e_ven = ttk.Entry(frame,width=7); e_ven.pack()

    def on_pay():
        tarjeta = {
            'numero': e_num.get().strip(),
            'cvv':    e_cvv.get().strip(),
            'vencimiento': e_ven.get().strip()
        }
        if simular_pago(inf['precio'], tarjeta):
            b = generar_boleto(inf)
            txt = "\n".join(f"{k}: {v}" for k,v in b.items())
            messagebox.showinfo("¡Pago OK!", txt)
            reserva_en_proceso = None
            mostrar_menu_principal()
        else:
            messagebox.showerror("Falló pago","Verifica datos tarjeta.")

    ttk.Button(frame, text="Pagar", command=on_pay).pack(pady=8)
    ttk.Button(frame, text="Volver", command=mostrar_menu_principal).pack()

# — Punto de entrada —
def iniciar_interfaz():
    global root
    root = tk.Tk()
    cargar_todos_los_datos()
    mostrar_login()
    root.mainloop()

if __name__ == "__main__":
    iniciar_interfaz()