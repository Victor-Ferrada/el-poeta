import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Funciones.gestion_bodega import crear_bodega
from Funciones.gestion_bodega import eliminar_bodega

# Función para gestionar bodegas 
def gestionar_bodegas():
    try:
        print("\nGestionar Bodegas")
        print("1. Crear Bodega")
        print("2. Eliminar Bodega")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            crear_bodega()
        elif opcion == "2":
            eliminar_bodega()
        else:
            raise ValueError("Opción no válida.")
    except ValueError as e:
        print(f"{e}, regresando al menú anterior.")