import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from os import system
import time
from Menus.menu_bodegas import gestionar_bodegas
from Funciones.gestionar_bodegas import Bodegas
bd=Bodegas()
from Funciones.gestionar_productos import Productos
p=Productos()
from Menus.menu_autores import gestionar_autores
from Menus.menu_editoriales import gestionar_editoriales
#from Funciones.generar_informe_de_inventario import generar_informe_inventario
#from Funciones.generar_informe_de_historial_de_movimientos import generar_informe_movimientos


# Menú del jefe de bodega
def menu_jefe_bodega(user):
    while True:
        try:
            print("\n--- Menú Jefe de Bodega ---\n")
            print("1. Gestionar Bodegas")
            print("2. Crear Productos")
            print("3. Gestionar Autores")
            print("4. Gestionar Editoriales")
            print("5. Visualizar todas las Bodegas")
            print("6. Generar Informe de Inventario")
            print("7. Generar Informe de Historial de Movimientos")
            print("8. Cerrar Sesión")
            opcion = input("\nSeleccione una opción: ")
            if opcion == "1":
                system('cls')
                gestionar_bodegas(user)
            elif opcion == "2":
                system('cls')
                p.agregar_producto()
            elif opcion == "3":
                system('cls')
                gestionar_autores()
            elif opcion == "4":
                system('cls')
                gestionar_editoriales(user)
            elif opcion == "5":
                system('cls')
                bd.mostrar_bodegas()
                input('Presione ENTER para volver atrás...')
                system('cls')
            elif opcion == "6":
                system('cls')
                #generar_informe_inventario()
            elif opcion == "7":
                system('cls')
                #generar_informe_movimientos()
            elif opcion == "8":
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
