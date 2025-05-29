"""
logica.py

Módulo con la lógica de negocio principal de Goodman Airlines.
Incluye autenticación, búsqueda y comparación de vuelos, gestión de reservas, simulación de pago y generación de boletos.
Pensado para funcionar con estructuras de datos provenientes de gestor_datos.py.
"""

import random
from datetime import datetime
from typing import List, Dict, Optional

def login(usuarios: List[Dict], usuario: str, contraseña: str) -> Optional[Dict]:
    """
    Valida las credenciales de un usuario.

    Args:
        usuarios (List[Dict]): Lista de usuarios (cada uno como dict con 'usuario', 'contraseña', etc.).
        usuario (str): Nombre de usuario a validar.
        contraseña (str): Contraseña proporcionada.

    Returns:
        Optional[Dict]: El dict del usuario si las credenciales son correctas, None en caso contrario.
    """
    for u in usuarios:
        if u.get('usuario') == usuario and u.get('contraseña') == contraseña:
            return u
    return None

def consultar_disponibilidad(vuelos: List[Dict], origen: str, destino: str, fecha: str) -> List[Dict]:
    """
    Filtra vuelos según origen, destino y fecha.

    Args:
        vuelos (List[Dict]): Lista de vuelos (cada uno como dict con 'origen', 'destino', 'fecha').
        origen (str): Ciudad de origen.
        destino (str): Ciudad de destino.
        fecha (str): Fecha del vuelo en formato 'YYYY-MM-DD'.

    Returns:
        List[Dict]: Lista de vuelos que cumplen con los criterios.
    """
    vuelos_disponibles = [
        v for v in vuelos
        if v.get('origen') == origen
        and v.get('destino') == destino
        and v.get('fecha', '')[:10] == fecha[:10]  # Acepta solo fecha (no hora)
    ]
    return vuelos_disponibles

def comparar_precios(lista_vuelos: List[Dict]) -> Optional[Dict]:
    """
    Ordena una lista de vuelos por precio y retorna el más barato.

    Args:
        lista_vuelos (List[Dict]): Lista de vuelos con atributo 'precio'.

    Returns:
        Optional[Dict]: El vuelo más barato o None si la lista está vacía.
    """
    if not lista_vuelos:
        return None
    return min(lista_vuelos, key=lambda v: v.get('precio', float('inf')))

def crear_reserva(usuario: Dict, vuelo: Dict, asiento: str) -> Dict:
    """
    Crea un objeto reserva con la información esencial.

    Args:
        usuario (Dict): Usuario que reserva.
        vuelo (Dict): Vuelo seleccionado.
        asiento (str): Código del asiento asignado.

    Returns:
        Dict: Objeto reserva listo para guardar o mostrar.
    """
    reserva = {
        "id_reserva": f"RES-{random.randint(100000, 999999)}",
        "usuario": usuario.get('usuario'),
        "vuelo_id": vuelo.get('id', vuelo.get('codigo', '')),
        "origen": vuelo.get('origen'),
        "destino": vuelo.get('destino'),
        "fecha": vuelo.get('fecha'),
        "asiento": asiento,
        "precio": vuelo.get('precio'),
        "fecha_reserva": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    return reserva

def simular_pago(monto: float, tarjeta: Dict) -> bool:
    """
    Simula el proceso de pago.

    Args:
        monto (float): Monto a cobrar.
        tarjeta (Dict): Información de la tarjeta ('numero', 'cvv', 'vencimiento').

    Returns:
        bool: True si el pago es exitoso, False si falla la validación básica o aleatoriamente.
    """
    # Validación muy básica
    numero = str(tarjeta.get('numero', ''))
    cvv = str(tarjeta.get('cvv', ''))
    vencimiento = tarjeta.get('vencimiento', '')

    if len(numero) < 13 or len(numero) > 19 or not numero.isdigit():
        return False
    if len(cvv) != 3 or not cvv.isdigit():
        return False
    try:
        vencimiento_dt = datetime.strptime(vencimiento, "%m/%y")
        if vencimiento_dt < datetime.now():
            return False
    except Exception:
        return False

    # Simulación aleatoria de éxito (90%)
    return random.random() < 0.9

def generar_boleto(reserva: Dict) -> Dict:
    """
    Genera un resumen del viaje (boleto) a partir de la reserva.

    Args:
        reserva (Dict): Objeto reserva.

    Returns:
        Dict: Resumen textual/diccionario del boleto.
    """
    boleto = {
        "Boleto": reserva.get("id_reserva"),
        "Pasajero": reserva.get("usuario"),
        "Vuelo": reserva.get("vuelo_id"),
        "Origen": reserva.get("origen"),
        "Destino": reserva.get("destino"),
        "Fecha de vuelo": reserva.get("fecha"),
        "Asiento": reserva.get("asiento"),
        "Precio": f"${reserva.get('precio'):.2f}",
        "Emitido": reserva.get("fecha_reserva")
    }
    return boleto

__all__ = [
    "login",
    "consultar_disponibilidad",
    "comparar_precios",
    "crear_reserva",
    "simular_pago",
    "generar_boleto"
]