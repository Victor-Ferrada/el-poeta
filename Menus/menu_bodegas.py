import sys
from os import system
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))                   #Esta ruta apunta al directorio padre del directorio donde se encuentra el script (Menus).
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'Funciones'))   #Esta ruta específica está dirigida al directorio Funciones, un nivel por encima del directorio donde se ejecuta el script (Menus).

from Funciones.gestionar_bodegas import Bodegas
bodegas=Bodegas()

# Función para gestionar bodegas 
def gestionar_bodegas(usuario):
    while True:
        try:
            print('-'*10+'Gestión de Bodegas'+'-'*10+'\n')
            print("1. Crear Bodega")
            print("2. Eliminar Bodega")
            print("3. Volver")
            opcion = input("\nSeleccione una opción: ")

            if opcion == "1":
                system('cls')
                bodegas.crear_bodega(usuario)
            elif opcion == "2":
                system('cls')
                bodegas.eliminar_bodega(usuario)
            elif opcion == "3":
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
