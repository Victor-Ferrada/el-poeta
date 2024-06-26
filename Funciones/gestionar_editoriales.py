import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Conexion_DB.conexion import conectar_db




# Función para eliminar una editorial
def eliminar_editorial():
    conexion = conectar_db()
    cursor = conexion.cursor()

    rutedit = input("Ingrese el RUT de la editorial a eliminar: ")
    cursor.execute("SELECT * FROM PRODUCTOS WHERE EDITORIAL = %s", (rutedit,))
    productos = cursor.fetchone()

    if productos:
        print("No se puede eliminar una editorial que tenga productos asociados.")
    else:
        cursor.execute("DELETE FROM EDITORIALES WHERE RUTEDIT = %s", (rutedit,))
        conexion.commit()
        print("Editorial eliminada exitosamente.")

# Función para agregar una editorial
def agregar_editorial():
    conexion = conectar_db()
    cursor = conexion.cursor()

    nombredit = input("Ingrese el nombre de la editorial: ")
    rutedit = input("Ingrese el RUT de la editorial: ")
    fonoedit = input("Ingrese el teléfono de la editorial: ")
    codpostedit = input("Ingrese el código postal de la editorial: ")
    represlegaldi = input("Ingrese el representante legal de la editorial: ")

    cursor.execute("INSERT INTO EDITORIALES (RUTEDIT, NOMBREDIT, FONOEDIT, CODPOSTEDIT, REPRESLEGALDI) VALUES (%s, %s, %s, %s, %s)",
                    (rutedit, nombredit, fonoedit, codpostedit, represlegaldi))
    conexion.commit()
    print("Editorial agregada exitosamente.")