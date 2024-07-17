import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from os import system
import time
from Funciones.otras_funciones import ConexionBD
bd=ConexionBD()
from Menus.menu_bodegas import menu_bodegas
from Funciones.gestionar_bodegas import Bodegas
from Funciones.informe_movimientos import generar_informe_movimientos
from Funciones.informe_inventario import generar_informe_inventario
bod=Bodegas()
from Menus.menu_productos import menu_productos
from Menus.menu_autores import gestionar_autores
from Menus.menu_editoriales import gestionar_editoriales

class JefeBodega():
    def __init__(self):
        self.conexion = ConexionBD.conectar_db()
        if self.conexion:
            self.cursor = self.conexion.cursor()
    
    # Menú del jefe de bodega
    def menu_jefe_bodega(self,user):
        locales=None
        while True:
            try:
                print("\n--- Menú Jefe de Bodega ---\n")
                print("1. Gestionar Bodegas")
                print("2. Gestionar Productos")
                print("3. Gestionar Autores")
                print("4. Gestionar Editoriales")
                print("5. Visualizar todas las Bodegas")
                print("6. Generar Informe de Inventario")
                print("7. Generar Informe de Historial de Movimientos")
                print("8. Cerrar Sesión")
                opcion = input("\nSeleccione una opción: ")
                if opcion == "1":
                    system('cls')
                    locales=menu_bodegas(user)
                elif opcion == "2":
                    system('cls')
                    menu_productos(user)
                elif opcion == "3":
                    system('cls')
                    gestionar_autores(user)
                elif opcion == "4":
                    system('cls')
                    gestionar_editoriales(user)
                elif opcion == "5":
                    system('cls')
                    bod.mostrar_bodegas()
                    input('Presione ENTER para volver atrás...')
                    system('cls')
                elif opcion == "6":
                    system('cls')
                    generar_informe_inventario()
                elif opcion == "7":
                    system('cls')
                    generar_informe_movimientos()
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
                        return locales
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

j=JefeBodega()
j.menu_jefe_bodega('123')