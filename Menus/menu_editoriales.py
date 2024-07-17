import sys
import os
from os import system
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))                   #Esta ruta apunta al directorio padre del directorio donde se encuentra el script (Menus).
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'Funciones'))   #Esta ruta específica está dirigida al directorio Funciones, un nivel por encima del directorio donde se ejecuta el script (Menus).

from Funciones.gestionar_editoriales import Editoriales
editoriales=Editoriales()
# Función para gestionar editoriales
def gestionar_editoriales(usuario):
    while True:
        try:
            print('-'*10+'Gestión de Editoriales'+'-'*10+'\n')
            print("1. Agregar Editorial")
            print("2. Visualizar Editoriales")
            print("3. Eliminar Editorial")
            print("4. Volver")
            opcion = input("\nSeleccione una opción: ")

            if opcion == "1":
                system('cls')
                editoriales.agregar_editorial()
            elif opcion == "2":
                system('cls')
                editoriales.mostrar_editoriales()
                input('Presione ENTER para volver atrás...')
                system('cls')
            elif opcion == "3":
                system('cls')
                editoriales.eliminar_editorial(usuario)  
            elif opcion == "4":
                system('cls')
                print("Volviendo al menú principal...")
                return
            else:
                system('cls')
                raise ValueError("Opción inválida.")
        except ValueError as e:
            print(f"{e} Ingrese una opción de la lista:")
        except Exception as e:
            print(f"Error inesperado: {e}")
            return

gestionar_editoriales('123')