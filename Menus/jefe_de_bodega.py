import sys
import os
import time
from os import system
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Funciones.otras_funciones import ConexionBD,save_locales
bd=ConexionBD()
from Menus.menu_bodegas import menu_bodegas
from Funciones.gestionar_bodegas import Bodegas as bod
from Funciones.informe_movimientos import generar_informe_movimientos
from Funciones.informe_inventario import generar_informe_inventario
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
        locales = None
        actualizar_locales = False
        while True:
            try:
                print("\n--- Menú Jefe de Bodega ---\n")
                print("1. Gestionar Bodegas")
                print("2. Gestionar Productos")
                print("3. Gestionar Autores")
                print("4. Gestionar Editoriales")
                print("5. Visualizar todas las Bodegas")
                print("6. Cerrar Sesión")
                opcion = input("\nSeleccione una opción: ")
                if opcion == "1":
                    system('cls')
                    nuevo_locales = menu_bodegas(user)
                    if nuevo_locales:
                        locales = nuevo_locales  # Actualizar locales solo si se crea una bodega nueva exitosamente
                        actualizar_locales = True
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
                    print("1. Generar Informe de Inventario")
                    print("2. Generar Informe de Historial de Movimientos")
                    print("3. Volver")
                    while True:
                        try:
                            opcion2 = input("\nSeleccione una opción: ")
                            if opcion2 == "1":
                                system('cls')
                                generar_informe_inventario()
                                bod.mostrar_bodegas()
                                print("1. Generar Informe de Inventario")
                                print("2. Generar Informe de Historial de Movimientos")
                                print("3. Volver")
                            elif opcion2 == "2":
                                system('cls')
                                generar_informe_movimientos()
                                bod.mostrar_bodegas()
                                print("1. Generar Informe de Inventario")
                                print("2. Generar Informe de Historial de Movimientos")
                                print("3. Volver")
                            elif opcion2 == "3":
                                system('cls')
                                break
                            else:
                                system('cls')
                                bod.mostrar_bodegas()
                                print("Opción inválida. Ingrese una opción de la lista: \n")
                                print("1. Generar Informe de Inventario")
                                print("2. Generar Informe de Historial de Movimientos")
                                print("3. Volver")
                        except Exception as e:
                            print(f"Error inesperado: {e}")
                            return
                elif opcion == "6":
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
                        if actualizar_locales:
                            save_locales(locales)  # Guardar locales solo si se han realizado cambios
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
                return locales
        
j=JefeBodega()
