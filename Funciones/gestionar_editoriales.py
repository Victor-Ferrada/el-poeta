import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import mysql.connector
from tabulate import tabulate


class Editoriales():
    def __init__(self):
         self.conexion = mysql.connector.connect(
             host='localhost',
             user='root',
             password='inacap2023',
             database='elpoeta')
         self.cursor = self.conexion.cursor()

    # Función para agregar una editorial
    def agregar_editorial(self):
        nombredit = input("Ingrese el nombre de la editorial: ").upper()
        rutedit = input("Ingrese el RUT de la editorial: ").upper()
        fonoedit = input("Ingrese el teléfono de la editorial: ")        #indicar tipo int
        codpostedit = input("Ingrese el código postal de la editorial: ")
        represlegaldi = input("Ingrese el representante legal de la editorial: ").upper()
        try:
            self.cursor.execute("INSERT INTO EDITORIALES (RUTEDIT, NOMEDIT, FONOEDI, CODPOSTEDI, REPRELEGEDI) VALUES (%s, %s, %s, %s, %s)",(rutedit, nombredit, fonoedit, codpostedit, represlegaldi))
            self.conexion.commit()
            print("\nEditorial agregada exitosamente.\n")
        except Exception as e:
            print(f"Error al agregar editorial: {e}")
            self.conexion.rollback()

    # Función para mostrar una editorial
    def mostrar_editoriales(self):
        sql='select * from editoriales'
        try:
            self.cursor.execute(sql)
            lista=self.cursor.fetchall()  
            print(tabulate(lista,headers=['Rut Edit.','Nombre','Teléfono','Cod. Postal','Representante Legal'],tablefmt='fancy_grid')) 
            print("\n")
        except Exception as e:
            print(f"Error al mostrar editoriales: {e}")
            self.conexion.rollback()

    # Función para eliminar una editorial
    def eliminar_editorial(self):
        Editoriales().mostrar_editoriales()
        rutedit = input("Ingrese el RUT de la editorial a eliminar: ").upper()
        self.cursor.execute("SELECT * FROM PRODUCTOS WHERE EDITORIAL = %s", (rutedit,))
        productos = self.cursor.fetchone()
        self.cursor.execute("SELECT * FROM EDITORIALES WHERE rutedit = %s", (rutedit,))
        editoriales = self.cursor.fetchone()
        while not editoriales:
            rutedit = input(f"Editorial {rutedit} no existe. Ingrese RUT nuevamente (o 's' para finalizar): ").upper()
            if rutedit=='S':
                print("\nOperación cancelada.\n")
                return
            self.cursor.execute("SELECT * FROM EDITORIALES WHERE RUTEDIT = %s", (rutedit,))
            editoriales = self.cursor.fetchone()
        if productos:
            print("\nNo se puede eliminar una editorial que tenga productos asociados.\n")
        else:
            try:
                self.cursor.execute("DELETE FROM EDITORIALES WHERE RUTEDIT = %s", (rutedit,))
                self.conexion.commit()
                print("\n")
                Editoriales().mostrar_editoriales()
                print("\nEditorial eliminada exitosamente.\n")
            except Exception as e:
                print(f"Error al eliminar editorial: {e}")
                self.conexion.rollback()

editoriales=Editoriales()
