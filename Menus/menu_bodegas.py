import sys
from os import system
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))                   #Esta ruta apunta al directorio padre del directorio donde se encuentra el script (Menus).
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'Funciones'))   #Esta ruta específica está dirigida al directorio Funciones, un nivel por encima del directorio donde se ejecuta el script (Menus).

from Funciones.gestionar_bodegas import Bodegas
from Funciones.gestionar_productos import Inventario
bod=Bodegas()
inv=Inventario()

# Función para gestionar bodegas 
def menu_bodegas(usuario,locales):
    locales=None
    while True:
        try:
            print('-'*10+'Gestión de Bodegas'+'-'*10+'\n')
            print("1. Crear Bodega")
            print("2. Añadir Productos a la Bodega")
            print("3. Mostrar Bodegas")
            print("4. Eliminar Bodega")
            print("5. Volver")
            opcion = input("\nSeleccione una opción: ")

            if opcion == "1":
                system('cls')
                locales=bod.crear_bodega(usuario)
            elif opcion == "2":
                system('cls')
                inv.añadir_productos(usuario,locales)
            elif opcion == "3":
                system('cls')
                bod.mostrar_bodegas()
                input('Presione ENTER para volver atrás...')
            elif opcion == "4":
                system('cls')
                bod.eliminar_bodega(usuario)
            elif opcion == "5":
                system('cls')
                print("Volviendo al menú principal...")
                return locales
            else:
                system('cls')
                raise ValueError("Opción inválida.")
        except ValueError as e:
            print(f"{e} Ingrese una opción de la lista:")
        except Exception as e:
            print(f"Error inesperado: {e}")
            return

