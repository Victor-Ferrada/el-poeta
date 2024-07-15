import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from os import system
import time
from Menus.menu_bodegas import gestionar_bodegas
from Funciones.gestion_bodega import Bodegas
bd=Bodegas()
from Funciones.crear_producto import crear_producto 
from Funciones.mover_productos import mover_productos
from gestion_autores import gestionar_autores
from Menus.menu_editoriales import gestionar_editoriales
from Funciones.generar_informe_de_inventario import generar_informe_inventario
from Funciones.generar_informe_de_historial_de_movimientos import generar_informe_movimientos


# Menú del jefe de bodega
def menu_jefe_bodega():
    while True:
        try:
            print("\n--- Menú Jefe de Bodega ---\n")
            print("1. Gestionar Bodegas")
            print("2. Crear Productos")
            print("3. Mover Productos")
            print("4. Gestionar Autores")
            print("5. Gestionar Editoriales")
            print("6. Visualizar todas las Bodegas")
            print("7. Generar Informe de Inventario")
            print("8. Generar Informe de Historial de Movimientos")
            print("9. Cerrar Sesión")
            opcion = input("\nSeleccione una opción: ")
            if opcion == "1":
                system('cls')
                gestionar_bodegas()
            elif opcion == "2":
                system('cls')
                crear_producto()
            elif opcion == "3":
                system('cls')
                mover_productos()
            elif opcion == "4":
                system('cls')
                gestionar_autores()
            elif opcion == "5":
                system('cls')
                gestionar_editoriales()
            elif opcion == "6":
                system('cls')
                bd.mostrar_bodegas()
                input('Presione ENTER para volver atrás...')
                system('cls')
            elif opcion == "7":
                system('cls')
                generar_informe_inventario()
            elif opcion == "8":
                system('cls')
                generar_informe_movimientos()
            elif opcion == "9":
                system('cls')
                confirmar=input('¿Está seguro que desea cerrar la sesión? (s/n): ')
                while confirmar not in ['s', 'n']:
                    confirmar = input("\nOpción inválida. Ingrese una opción válida (s/n): ").lower()
                if confirmar=='s':
                    for i in range(3, 0, -1):
                        system('cls')
                        print(f"Cerrando sesión en {i} segundos...", end='\r')
                        time.sleep(1)  
                    system('cls')
                    return 
                else:
                    system('cls')
                    continue
            else:
                system('cls')
                raise ValueError("Opción inválida.")
        except ValueError as e:
            print(f"{e} Ingrese una opción de la lista:")
        except Exception as e:
            print(f"Error inesperado: {e}")
            return
        
menu_jefe_bodega()