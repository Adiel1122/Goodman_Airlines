"""
interfaz.py

Módulo de interfaz gráfica para Goodman Airlines.
Utiliza Tkinter y ttk para mostrar menús, formularios y resultados.
Incluye manejo de login, consulta de vuelos, reserva, pago y mensajes.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from gestor_datos import cargar_vuelos, cargar_usuarios, cargar_reservas, guardar_reservas
from logica import (
    login, consultar_disponibilidad, comparar_precios, crear_reserva, simular_pago, generar_boleto
)
from algoritmos import asignar_asiento_greedy

class AplicacionAereolinea:
    def __init__(self, root):
        self.root = root
        self.root.title("Goodman Airlines")
        self.usuario_actual = None
        self.vuelos = self._cargar_vuelos_lista()
        self.usuarios = self._cargar_usuarios_lista()
        self.reservas = self._cargar_reservas_lista()
        self.reserva_en_proceso = None
        self._mostrar_login()

    def _cargar_vuelos_lista(self):
        df = cargar_vuelos()
        return df.to_dict('records') if not df.empty else []

    def _cargar_usuarios_lista(self):
        df = cargar_usuarios()
        return df.to_dict('records') if not df.empty else []

    def _cargar_reservas_lista(self):
        df = cargar_reservas()
        return df.to_dict('records') if not df.empty else []

    def _mostrar_login(self):
        self._limpiar_ventana()
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(expand=True)

        ttk.Label(frame, text="Iniciar sesión", font=('Arial', 14, 'bold')).pack(pady=8)

        ttk.Label(frame, text="Usuario:").pack(anchor='w')
        entry_usuario = ttk.Entry(frame)
        entry_usuario.pack(fill='x')

        ttk.Label(frame, text="Contraseña:").pack(anchor='w')
        entry_contraseña = ttk.Entry(frame, show="*")
        entry_contraseña.pack(fill='x')

        def intentar_login():
            usuario = entry_usuario.get()
            contraseña = entry_contraseña.get()
            user = login(self.usuarios, usuario, contraseña)
            if user:
                self.usuario_actual = user
                self.mostrar_menu_principal()
            else:
                messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

        ttk.Button(frame, text="Ingresar", command=intentar_login).pack(pady=10)

    def mostrar_menu_principal(self):
        self._limpiar_ventana()

        # --- Imagen de fondo ---
        from PIL import Image, ImageTk  # Asegúrate de tener pillow: pip install pillow

        fondo_path = "fondoMenu.jpg"  # Cambia aquí el nombre si tu imagen se llama diferente
        ancho, alto = 600, 400

        # Cargar imagen y ajustarla
        try:
            imagen = Image.open(fondo_path)
            imagen = imagen.resize((ancho, alto), Image.LANCZOS)
            self._fondo_img = ImageTk.PhotoImage(imagen)
        except Exception as e:
            # Si falla, solo usa color de fondo liso
            self._fondo_img = None

        canvas = tk.Canvas(self.root, width=ancho, height=alto, highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        if self._fondo_img:
            canvas.create_image(0, 0, anchor="nw", image=self._fondo_img)
        else:
            canvas.create_rectangle(0, 0, ancho, alto, fill="#b0e0ff", outline="")

        # --- Frame encima del canvas (para los widgets) ---
        frame = ttk.Frame(self.root, style="MenuPrincipal.TFrame")
        # Centra el frame usando place
        frame.place(relx=0.5, rely=0.5, anchor='center')

        ttk.Label(frame, text=f"Bienvenido/a, {self.usuario_actual.get('usuario', '')}",
                font=('Arial', 16, 'bold'), background="#b0e0ff").pack(pady=15)

        btns = [
            ("Consultar vuelos", self.consultar_vuelos),
            ("Reservar vuelo", self.reservar_vuelo),
            ("Pagar", self.pagar_reserva),
            ("Salir", self.root.quit)
        ]

        # --- Animación elaborada de "Cargando..." con puntos ---
        def animar_y_llamar(funcion):
            cargando = ttk.Label(frame, text="Cargando", font=('Arial', 13, 'italic'), foreground="#2573b9")
            cargando.pack(pady=10)
            puntos = ["", ".", "..", "...", "....", ".....", "......"]
            intervalo = 110  # milisegundos entre cada frame
            total_frames = len(puntos)

            def animar(frame=0):
                cargando.config(text="Cargando" + puntos[frame])
                if frame < total_frames - 1:
                    self.root.after(intervalo, animar, frame + 1)
                else:
                    cargando.config(text="¡Listo!")
                    self.root.after(250, lambda: [cargando.destroy(), funcion()])

            animar()

        for texto, funcion in btns:
            ttk.Button(frame, text=texto, width=25,
                    command=lambda f=funcion: animar_y_llamar(f)).pack(pady=6)

        # Opcional: estilo para el frame
        estilo = ttk.Style()
        estilo.configure("MenuPrincipal.TFrame", background="#b0e0ff", relief="flat")

    def consultar_vuelos(self):
        self._limpiar_ventana()
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(expand=True, fill='both')

        ttk.Label(frame, text="Consulta de vuelos", font=('Arial', 12, 'bold')).pack(pady=8)

        frm_filtros = ttk.Frame(frame)
        frm_filtros.pack(pady=5)

        ttk.Label(frm_filtros, text="Origen:").grid(row=0, column=0)
        entry_origen = ttk.Entry(frm_filtros, width=10)
        entry_origen.grid(row=0, column=1, padx=4)

        ttk.Label(frm_filtros, text="Destino:").grid(row=0, column=2)
        entry_destino = ttk.Entry(frm_filtros, width=10)
        entry_destino.grid(row=0, column=3, padx=4)

        ttk.Label(frm_filtros, text="Fecha (YYYY-MM-DD):").grid(row=0, column=4)
        entry_fecha = ttk.Entry(frm_filtros, width=12)
        entry_fecha.grid(row=0, column=5, padx=4)

        tree = ttk.Treeview(frame, columns=("origen", "destino", "fecha", "hora", "precio"), show='headings', height=10)
        for col in ("origen", "destino", "fecha", "hora", "precio"):
            tree.heading(col, text=col.capitalize())
            tree.column(col, width=90, anchor='center')
        tree.pack(fill='both', expand=True, pady=8)

        def buscar():
            origen = entry_origen.get().strip()
            destino = entry_destino.get().strip()
            fecha = entry_fecha.get().strip()
            if not (origen and destino and fecha):
                messagebox.showwarning("Campos necesarios", "Debe ingresar origen, destino y fecha.")
                return
            resultados = consultar_disponibilidad(self.vuelos, origen, destino, fecha)
            for row in tree.get_children():
                tree.delete(row)
            if not resultados:
                messagebox.showinfo("Sin resultados", "No se encontraron vuelos.")
            for v in resultados:
                fecha_vuelo = v.get('fecha', '')[:10]
                hora_vuelo = v.get('fecha', '')[11:16]
                tree.insert('', 'end', values=(
                    v.get('origen'),
                    v.get('destino'),
                    fecha_vuelo,
                    hora_vuelo,
                    f"${v.get('precio', 0):.2f}"
                ))

        ttk.Button(frm_filtros, text="Buscar", command=buscar).grid(row=0, column=6, padx=4)
        ttk.Button(frame, text="Volver", command=self.mostrar_menu_principal).pack(pady=6)

    def reservar_vuelo(self):
        self._limpiar_ventana()
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(expand=True, fill='both')

        ttk.Label(frame, text="Reservar vuelo", font=('Arial', 12, 'bold')).pack(pady=8)

        # Selección de vuelo
        ttk.Label(frame, text="Seleccione vuelo:").pack()
        vuelos_combo = ttk.Combobox(frame, width=60, state="readonly")
        vuelos_combo.pack()

        vuelos_mostrar = [
            f"{v['origen']} → {v['destino']} | {v['fecha']} | ${v['precio']:.2f}" for v in self.vuelos
        ]
        vuelos_combo['values'] = vuelos_mostrar

        # Selección de asiento
        ttk.Label(frame, text="Seleccione asiento:").pack(pady=4)
        asientos_combo = ttk.Combobox(frame, width=20, state="readonly")
        asientos_combo.pack()

        def actualizar_asientos(event=None):
            idx = vuelos_combo.current()
            if idx == -1:
                asientos_combo['values'] = []
                return
            vuelo_sel = self.vuelos[idx]
            # Se asume que 'asientos_disponibles' es lista de dicts {'codigo', 'precio'}
            asientos = vuelo_sel.get('asientos_disponibles', [])
            if not asientos:
                asientos_combo['values'] = ["No hay asientos"]
            else:
                asientos_combo['values'] = [f"{a['codigo']} (${a['precio']:.2f})" for a in asientos]
                # Selecciona el más barato por defecto
                asientos_combo.current(0)

        vuelos_combo.bind("<<ComboboxSelected>>", actualizar_asientos)

        def reservar():
            idx_vuelo = vuelos_combo.current()
            idx_asiento = asientos_combo.current()
            if idx_vuelo == -1 or idx_asiento == -1:
                messagebox.showwarning("Seleccione", "Debe elegir un vuelo y asiento.")
                return
            vuelo = self.vuelos[idx_vuelo]
            asientos = vuelo.get('asientos_disponibles', [])
            if not asientos:
                messagebox.showerror("Sin asientos", "Este vuelo no tiene asientos disponibles.")
                return
            asiento = asientos[idx_asiento]['codigo']
            reserva = crear_reserva(self.usuario_actual, vuelo, asiento)
            self.reserva_en_proceso = reserva
            # Simula guardar la reserva
            self.reservas.append(reserva)
            guardar_reservas(self._crear_reservas_dataframe())
            messagebox.showinfo("Reserva exitosa", f"Reserva creada: {reserva['id_reserva']}. Proceda al pago.")
            self.mostrar_menu_principal()

        ttk.Button(frame, text="Reservar", command=reservar).pack(pady=8)
        ttk.Button(frame, text="Volver", command=self.mostrar_menu_principal).pack()

    def pagar_reserva(self):
        self._limpiar_ventana()
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(expand=True)

        ttk.Label(frame, text="Pago de reserva", font=('Arial', 12, 'bold')).pack(pady=8)

        if not self.reserva_en_proceso:
            ttk.Label(frame, text="No hay reserva pendiente para pagar.").pack(pady=6)
            ttk.Button(frame, text="Volver", command=self.mostrar_menu_principal).pack()
            return

        ttk.Label(frame, text=f"Reserva: {self.reserva_en_proceso['id_reserva']} | Monto: ${self.reserva_en_proceso['precio']:.2f}").pack(pady=5)
        ttk.Label(frame, text="Número de tarjeta:").pack(anchor='w')
        entry_numero = ttk.Entry(frame)
        entry_numero.pack(fill='x')
        ttk.Label(frame, text="CVV:").pack(anchor='w')
        entry_cvv = ttk.Entry(frame, width=5)
        entry_cvv.pack()
        ttk.Label(frame, text="Vencimiento (MM/YY):").pack(anchor='w')
        entry_venc = ttk.Entry(frame, width=7)
        entry_venc.pack()

        def pagar():
            tarjeta = {
                'numero': entry_numero.get().strip(),
                'cvv': entry_cvv.get().strip(),
                'vencimiento': entry_venc.get().strip()
            }
            monto = self.reserva_en_proceso['precio']
            exito = simular_pago(monto, tarjeta)
            if exito:
                boleto = generar_boleto(self.reserva_en_proceso)
                messagebox.showinfo(
                    "¡Pago exitoso!",
                    f"Boleto emitido:\n\n"
                    f"Reserva: {boleto['Boleto']}\n"
                    f"Pasajero: {boleto['Pasajero']}\n"
                    f"Vuelo: {boleto['Vuelo']}\n"
                    f"Origen: {boleto['Origen']}\n"
                    f"Destino: {boleto['Destino']}\n"
                    f"Asiento: {boleto['Asiento']}\n"
                    f"Fecha: {boleto['Fecha de vuelo']}\n"
                    f"Precio: {boleto['Precio']}\n"
                    f"Emitido: {boleto['Emitido']}"
                )
                self.reserva_en_proceso = None
                self.mostrar_menu_principal()
            else:
                messagebox.showerror("Pago fallido", "No se pudo procesar el pago. Verifique los datos.")

        ttk.Button(frame, text="Pagar", command=pagar).pack(pady=8)
        ttk.Button(frame, text="Volver", command=self.mostrar_menu_principal).pack()

    def _limpiar_ventana(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def _crear_reservas_dataframe(self):
        # Convierte la lista de reservas a DataFrame para guardar fácilmente
        import pandas as pd
        return pd.DataFrame(self.reservas)

# Función para lanzar la app desde main.py
def iniciar_interfaz():
    root = tk.Tk()
    app = AplicacionAereolinea(root)
    root.mainloop()

__all__ = ["iniciar_interfaz"]