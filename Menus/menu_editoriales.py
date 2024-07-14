import sys
import os
from os import system
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))                   #Esta ruta apunta al directorio padre del directorio donde se encuentra el script (Menus).
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'Funciones'))   #Esta ruta específica está dirigida al directorio Funciones, un nivel por encima del directorio donde se ejecuta el script (Menus).

from Funciones.gestionar_editoriales import Editoriales
editoriales=Editoriales()
# Función para gestionar editoriales
def gestionar_editoriales():
    while True:
        try:
            print('-'*10+'Gestión de Editoriales'+'-'*10+'\n')
            print("1. Agregar Editorial")
            print("2. Eliminar Editorial")
            print("3. Salir")
            opcion = input("\nSeleccione una opción: ")

            if opcion == "1":
                system('cls')
                editoriales.agregar_editorial()
            elif opcion == "2":
                system('cls')
                editoriales.eliminar_editorial()
            elif opcion == "3":
                system('cls')
                print("Volviendo al menú principal...")
                return
            else:
                raise ValueError("Opción no válida.")
        except ValueError as e:
            print(f"{e}, regresando al menú anterior.")
        except Exception as e:
            print(f"Error inesperado: {e}")
            return

gestionar_editoriales()