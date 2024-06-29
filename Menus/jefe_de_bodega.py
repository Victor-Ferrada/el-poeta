import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Funciones.cls import cls

from gestion_bodegas import gestionar_bodegas
from Funciones.crear_producto import crear_producto 
from Funciones.mover_productos import mover_productos
from gestion_autores import gestionar_autores
from gestion_editoria import gestionar_editoriales
from Funciones.visualizar_todas_las_bodegas import visualizar_bodegas
from Funciones.generar_informe_de_inventario import generar_informe_inventario
from Funciones.generar_informe_de_historial_de_movimientos import generar_informe_movimientos

# Menú del jefe de bodega
def menu_jefe_bodega():
    while True:
        print("\n--- Menú Jefe de Bodega ---")
        print("1. Gestionar Bodegas")
        print("2. Crear Productos")
        print("3. Mover Productos")
        print("4. Gestionar Autores")
        print("5. Gestionar Editoriales")
        print("6. Visualizar todas las Bodegas")
        print("7. Generar Informe de Inventario")
        print("8. Generar Informe de Historial de Movimientos")
        print("9. Cerrar Sesión")
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            cls()
            gestionar_bodegas()
        elif opcion == "2":
            cls()
            crear_producto()
        elif opcion == "3":
            cls()
            mover_productos()
        elif opcion == "4":
            cls()
            gestionar_autores()
        elif opcion == "5":
            cls()
            gestionar_editoriales()
        elif opcion == "6":
            cls()
            visualizar_bodegas()
        elif opcion == "7":
            cls()
            generar_informe_inventario()
        elif opcion == "8":
            cls()
            generar_informe_movimientos()
        elif opcion == "9":
            print("Cerrando sesión...")
            cls()
            break
        else:
            print("Opción no válida. Por favor, seleccione una opción del menú.")
