"""
algoritmos.py

Módulo que contiene algoritmos de utilidad para la gestión de vuelos:
- QuickSort genérico para ordenar listas de objetos por cualquier atributo.
- Asignación de asientos mediante algoritmo greedy.
- Búsqueda recursiva de rutas entre ciudades (función placeholder).
"""

from typing import List, Callable, Any, Dict, Optional

def quicksort(objetos: List[Any], key: Callable[[Any], Any]) -> List[Any]:
    """
    Ordena una lista de objetos utilizando el algoritmo QuickSort y una función clave.

    Args:
        objetos (List[Any]): Lista de objetos a ordenar.
        key (Callable[[Any], Any]): Función que extrae el valor a comparar de cada objeto.

    Returns:
        List[Any]: Nueva lista de objetos ordenada según el atributo especificado.
    """
    if len(objetos) <= 1:
        return objetos[:]
    else:
        pivote = objetos[0]
        menores = [obj for obj in objetos[1:] if key(obj) <= key(pivote)]
        mayores = [obj for obj in objetos[1:] if key(obj) > key(pivote)]
        return quicksort(menores, key) + [pivote] + quicksort(mayores, key)


def asignar_asiento_greedy(vuelo: Dict, usuario: Dict) -> Optional[str]:
    """
    Asigna el mejor asiento disponible en un vuelo utilizando un criterio simple (ej: más barato).

    Args:
        vuelo (Dict): Diccionario con información del vuelo, debe contener una lista de asientos disponibles
                      bajo la clave 'asientos_disponibles', donde cada asiento es un diccionario con 'codigo', 'precio', etc.
        usuario (Dict): Diccionario con información del usuario (puede usarse para criterios futuros).

    Returns:
        Optional[str]: Código del asiento asignado, o None si no hay asientos disponibles.
    """
    asientos = vuelo.get('asientos_disponibles', [])
    if not asientos:
        return None

    # Ejemplo: asignar el asiento más barato
    asiento_seleccionado = min(asientos, key=lambda a: a.get('precio', float('inf')))
    return asiento_seleccionado.get('codigo')


def buscar_ruta_recursiva(origen: str, destino: str, vuelos: List[Dict], ruta_actual=None, visitados=None) -> List[List[Dict]]:
    """
    Busca rutas recursivamente entre dos ciudades usando los vuelos disponibles.
    Esta es una implementación simple que retorna todas las rutas posibles (sin ciclos).

    Args:
        origen (str): Ciudad de origen.
        destino (str): Ciudad de destino.
        vuelos (List[Dict]): Lista de vuelos (cada uno como dict con claves 'origen', 'destino').
        ruta_actual (List[Dict], opcional): Ruta construida hasta el momento.
        visitados (set, opcional): Ciudades ya visitadas en la ruta actual.

    Returns:
        List[List[Dict]]: Lista de rutas posibles, cada una como lista de vuelos (dicts).
    """
    if ruta_actual is None:
        ruta_actual = []
    if visitados is None:
        visitados = set()

    rutas = []
    for vuelo in vuelos:
        if vuelo['origen'] == origen and vuelo['destino'] not in visitados:
            nueva_ruta = ruta_actual + [vuelo]
            if vuelo['destino'] == destino:
                rutas.append(nueva_ruta)
            else:
                nuevas_rutas = buscar_ruta_recursiva(
                    vuelo['destino'],
                    destino,
                    vuelos,
                    nueva_ruta,
                    visitados | {origen}
                )
                rutas.extend(nuevas_rutas)
    return rutas

__all__ = [
    "quicksort",
    "asignar_asiento_greedy",
    "buscar_ruta_recursiva",
]