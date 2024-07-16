import sys
from os import system
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))                   #Esta ruta apunta al directorio padre del directorio donde se encuentra el script (Menus).
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'Funciones'))   #Esta ruta específica está dirigida al directorio Funciones, un nivel por encima del directorio donde se ejecuta el script (Menus).


from Funciones.gestionar_productos import Inventario,Productos
inv=Inventario()
prod=Productos()

# Función para gestionar productos 
def menu_productos(usuario):
    while True:
        try:
            print('-'*10+'Gestión de Productos'+'-'*10+'\n')
            print("1. Agregar Producto")
            print("2. Mostrar Productos")
            print("3. Añadir a Bodega")
            print("4. Eliminar Producto")
            print("5. Volver")
            opcion = input("\nSeleccione una opción: ")

            if opcion == '1':
                system('cls')
                prod.agregar_producto(usuario)
            elif opcion == '2':
                system('cls')
                prod.mostrar_productos()
            elif opcion == '3':
                system('cls')
                inv.añadir_productos(usuario)
            elif opcion == '4':
                system('cls')
                prod.eliminar_producto(usuario)
            elif opcion == '5':
                system('cls')
                print("Volviendo al menú principal...")
                break
            else:
                system('cls')
                raise ValueError("Opción inválida.")
        except ValueError as e:
            print(f"{e} Ingrese una opción de la lista:")
        except Exception as e:
            print(f"Error inesperado: {e}")
            return
