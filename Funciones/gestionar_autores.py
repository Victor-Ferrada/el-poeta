import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Conexion_DB.conexion import conectar_db

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

# Función para agregar un autor
def agregar_autor():
    conexion = conectar_db()
    cursor = conexion.cursor()

    nombres_au = input("Ingrese los nombres del autor: ")
    app_aut = input("Ingrese el apellido paterno del autor: ")
    amp_aut = input("Ingrese el apellido materno del autor: ")
    cod_post_au = input("Ingrese el código postal del autor: ")
    fono_au = input("Ingrese el teléfono del autor: ")
    run_autor = input("Ingrese el RUT del autor: ")

    cursor.execute("INSERT INTO AUTORES (RUNAUTOR, NOMBRESAU, APPAUT, AMPAUT, CODPOSTAU, FONOAU) VALUES (%s, %s, %s, %s, %s, %s)",
                    (run_autor, nombres_au, app_aut, amp_aut, cod_post_au, fono_au))
    conexion.commit()
    print("Autor agregado exitosamente.")
# Función para eliminar un autor
def eliminar_autor():
    conexion = conectar_db()
    cursor = conexion.cursor()

    run_autor = input("Ingrese el RUT del autor a eliminar: ")
    cursor.execute("SELECT * FROM AUPROD WHERE RUNAUTOR = %s", (run_autor,))
    productos = cursor.fetchone()

    if productos:
        print("No se puede eliminar un autor que tenga productos asociados.")
    else:
        cursor.execute("DELETE FROM AUTORES WHERE RUNAUTOR = %s", (run_autor,))
        conexion.commit()
        print("Autor eliminado exitosamente.")
