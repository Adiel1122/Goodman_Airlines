"""
gestor_datos.py

Módulo para la gestión de datos de vuelos, usuarios y reservas utilizando archivos Excel (.xlsx).
Utiliza pandas y openpyxl para la manipulación de los archivos.
Provee funciones para cargar y guardar cada tipo de dato, manejando errores comunes de E/S.
"""

import os
import pandas as pd

# Rutas por defecto de los archivos Excel
ARCHIVO_VUELOS = "vuelos.xlsx"
ARCHIVO_USUARIOS = "usuarios.xlsx"
ARCHIVO_RESERVAS = "reservas.xlsx"

def cargar_vuelos(ruta=ARCHIVO_VUELOS):
    """
    Carga los datos de vuelos desde un archivo Excel.
    
    Args:
        ruta (str): Ruta al archivo Excel de vuelos.
        
    Returns:
        pd.DataFrame: DataFrame con los datos de los vuelos.
                      Si el archivo no existe o es ilegible, retorna un DataFrame vacío.
    """
    try:
        if not os.path.exists(ruta):
            print(f"[INFO] Archivo de vuelos '{ruta}' no encontrado. Se creará uno nuevo al guardar.")
            return pd.DataFrame()
        df = pd.read_excel(ruta, engine="openpyxl")
        return df
    except Exception as e:
        print(f"[ERROR] No se pudo cargar el archivo de vuelos: {e}")
        return pd.DataFrame()

def guardar_vuelos(vuelos, ruta=ARCHIVO_VUELOS):
    """
    Guarda los datos de vuelos en un archivo Excel.
    
    Args:
        vuelos (pd.DataFrame): DataFrame con los datos de vuelos a guardar.
        ruta (str): Ruta al archivo Excel de vuelos.
    """
    try:
        vuelos.to_excel(ruta, index=False, engine="openpyxl")
        print(f"[OK] Vuelos guardados correctamente en '{ruta}'.")
    except Exception as e:
        print(f"[ERROR] No se pudo guardar el archivo de vuelos: {e}")

def cargar_usuarios(ruta=ARCHIVO_USUARIOS):
    """
    Carga los datos de usuarios desde un archivo Excel.
    
    Args:
        ruta (str): Ruta al archivo Excel de usuarios.
        
    Returns:
        pd.DataFrame: DataFrame con los datos de los usuarios.
                      Si el archivo no existe o es ilegible, retorna un DataFrame vacío.
    """
    try:
        if not os.path.exists(ruta):
            print(f"[INFO] Archivo de usuarios '{ruta}' no encontrado. Se creará uno nuevo al guardar.")
            return pd.DataFrame()
        df = pd.read_excel(ruta, engine="openpyxl")
        return df
    except Exception as e:
        print(f"[ERROR] No se pudo cargar el archivo de usuarios: {e}")
        return pd.DataFrame()

def guardar_usuarios(usuarios, ruta=ARCHIVO_USUARIOS):
    """
    Guarda los datos de usuarios en un archivo Excel.
    
    Args:
        usuarios (pd.DataFrame): DataFrame con los datos de usuarios a guardar.
        ruta (str): Ruta al archivo Excel de usuarios.
    """
    try:
        usuarios.to_excel(ruta, index=False, engine="openpyxl")
        print(f"[OK] Usuarios guardados correctamente en '{ruta}'.")
    except Exception as e:
        print(f"[ERROR] No se pudo guardar el archivo de usuarios: {e}")

def cargar_reservas(ruta=ARCHIVO_RESERVAS):
    """
    Carga los datos de reservas desde un archivo Excel.
    
    Args:
        ruta (str): Ruta al archivo Excel de reservas.
        
    Returns:
        pd.DataFrame: DataFrame con los datos de las reservas.
                      Si el archivo no existe o es ilegible, retorna un DataFrame vacío.
    """
    try:
        if not os.path.exists(ruta):
            print(f"[INFO] Archivo de reservas '{ruta}' no encontrado. Se creará uno nuevo al guardar.")
            return pd.DataFrame()
        df = pd.read_excel(ruta, engine="openpyxl")
        return df
    except Exception as e:
        print(f"[ERROR] No se pudo cargar el archivo de reservas: {e}")
        return pd.DataFrame()

def guardar_reservas(reservas, ruta=ARCHIVO_RESERVAS):
    """
    Guarda los datos de reservas en un archivo Excel.
    
    Args:
        reservas (pd.DataFrame): DataFrame con los datos de reservas a guardar.
        ruta (str): Ruta al archivo Excel de reservas.
    """
    try:
        reservas.to_excel(ruta, index=False, engine="openpyxl")
        print(f"[OK] Reservas guardadas correctamente en '{ruta}'.")
    except Exception as e:
        print(f"[ERROR] No se pudo guardar el archivo de reservas: {e}")

# Permite importar solo funciones útiles desde otros módulos
__all__ = [
    "cargar_vuelos", "guardar_vuelos",
    "cargar_usuarios", "guardar_usuarios",
    "cargar_reservas", "guardar_reservas"
]