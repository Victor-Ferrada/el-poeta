import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Funciones.gestionar_editoriales import agregar_editorial
from Funciones.gestionar_editoriales import eliminar_editorial

# Función para gestionar editoriales
def gestionar_editoriales():
    print("\nGestionar Editoriales")
    print("1. Agregar Editorial")
    print("2. Eliminar Editorial")
    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        agregar_editorial()
    elif opcion == "2":
        eliminar_editorial()
    else:
        print("Opción no válida, regresando al menú anterior.")