import sys
import os
from os import system
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))                   #Esta ruta apunta al directorio padre del directorio donde se encuentra el script (Menus).
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'Funciones'))   #Esta ruta específica está dirigida al directorio Funciones, un nivel por encima del directorio donde se ejecuta el script (Menus).

from Funciones.gestionar_autores import Autores
au=Autores()

# Función para gestionar autores 
def gestionar_autores(user):
    while True:
        try:
            print('-'*10+'Gestión de Autores'+'-'*10+'\n')
            print("1. Agregar Autor")
            print("2. Visualizar Autores")
            print("3. Eliminar Autor")
            print("4. Volver")
            opcion = input("\nSeleccione una opción: ")
            if opcion == "1":
                system('cls')
                au.agregar_autor()
            elif opcion == "2":
                system('cls')
                au.mostrar_autores()
                input('Presione ENTER para volver atrás...')
                system('cls')
            elif opcion == "3":
                system('cls')
                au.eliminar_autor(user)
            elif opcion == "4":
                system('cls')
                print("Volviendo al menú principal...")
                return
            else:
                system('cls')
                raise ValueError("Opción inválida.")
        except ValueError as e:
            print(f"{e} Ingrese una opción de la lista:")
        except Exception as e:
            print(f"Error inesperado: {e}")
            return