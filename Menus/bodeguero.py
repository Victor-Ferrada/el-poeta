import sys
import os
from os import system
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Funciones.mover_productos import mover_productos

# Menú del bodeguero
def menu_bodeguero():
    while True:
        try:
            print("\n--- Menú Bodeguero ---\n")
            print("1. Mover Productos")
            print("2. Cerrar Sesión")
            opcion = input("\nSeleccione una opción: ")

            if opcion == "1":
                mover_productos()
            elif opcion == "2":
                system('cls')
                for i in range(3, 0, -1):
                    print(f"Cerrando sesión en {i} segundos...", end='\r')
                    time.sleep(1)
                return
            else:
                system('cls')
                raise ValueError("Opción inválida.")
        except ValueError as e:
            print(f"{e} Ingrese una opción de la lista:")
        except Exception as e:
            print(f"Error inesperado: {e}")
            return
        
menu_bodeguero()