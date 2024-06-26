import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Funciones.gestionar_autores import agregar_autor
from Funciones.gestionar_autores import eliminar_autor

# Función para gestionar autores 
def gestionar_autores():
    print("\nGestionar Autores")
    print("1. Agregar Autor")
    print("2. Eliminar Autor")
    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        agregar_autor()
    elif opcion == "2":
        eliminar_autor()
    else:
        print("Opción no válida, regresando al menú anterior.")
