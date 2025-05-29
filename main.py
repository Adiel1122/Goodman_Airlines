"""
main.py

Punto de entrada para Goodman Airlines.
Carga los datos, integra todos los módulos y lanza la interfaz gráfica principal.
"""

import gestor_datos
import algoritmos
import logica
import interfaz

if __name__ == '__main__':
    # Los módulos de datos y lógica trabajan por defecto sobre los archivos .xlsx.
    # La interfaz se encarga de cargar los datos y lanzar el flujo principal.
    interfaz.iniciar_interfaz()