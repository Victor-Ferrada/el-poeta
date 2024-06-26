import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Funciones.mover_productos import mover_productos
from Funciones.visualizar_todas_las_bodegas import visualizar_bodegas

# Menú del bodeguero
def menu_bodeguero():
    while True:
        print("\n--- Menú Bodeguero ---")
        print("1. Mover Productos")
        print("2. Visualizar todas las Bodegas")
        print("3. Cerrar Sesión")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            mover_productos()
        elif opcion == "2":
            visualizar_bodegas()
        elif opcion == "3":
            print("Cerrando sesión...")
            break
        else:
            print("Opción no válida. Por favor, seleccione una opción del menú.")