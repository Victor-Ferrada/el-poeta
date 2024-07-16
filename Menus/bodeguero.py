import sys
import os
from os import system
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Funciones.otras_funciones import ConexionBD
bd=ConexionBD()
from Funciones.movimientos import Movimientos
mov=Movimientos()


class Bodeguero():
    def __init__(self):
        self.conexion = ConexionBD.conectar_db()
        if self.conexion:
            self.cursor = self.conexion.cursor()

    # Menú del bodeguero
    def menu_bodeguero(user,locales):
        while True:
            try:
                print("\n--- Menú Bodeguero ---\n")
                print("1. Mover Productos")
                print("2. Cerrar Sesión")
                opcion = input("\nSeleccione una opción: ")
                if opcion == "1":
                    mov.mover_producto(user,locales)
                elif opcion == "2":
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
