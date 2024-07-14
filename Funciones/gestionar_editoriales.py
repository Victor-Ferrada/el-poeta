import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import mysql.connector
from tabulate import tabulate
from otras_funciones import validar_entero

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
        while True:
            nombredit = input("Ingrese el nombre de la editorial: ").strip().upper()
            while nombredit=='':
                nombredit = input("El nombre de la editorial no puede estar vacío. Ingrese nuevamente: ").strip().upper()
            rutedit = input("Ingrese el RUT de la editorial: ").strip().upper()
            while rutedit=='':
                rutedit = input("El RUT de la editorial no puede estar vacío. Ingrese nuevamente: ").strip().upper()
            fonoedit = validar_entero("Ingrese el teléfono de la editorial: ",'teléfono')
            codpostedit = validar_entero("Ingrese el código postal de la editorial: ",'código postal')
            represlegaldi = input("Ingrese el representante legal de la editorial: ").strip().upper()
            self.cursor.execute("SELECT * FROM EDITORIALES WHERE RUTEDIT = %s", (rutedit,))
            editorial = self.cursor.fetchone()
            if editorial:
                print('\nLa editorial ingresada ya se encuentra registrada en el sistema. \n\nIngrese una nueva editorial o seleccione una existente volviendo atrás.')
                opcion=input('\n¿Ingresar nueva editorial? (s/n): ')
                if opcion=='s':
                    continue
                elif opcion=='n':
                    print("\nOperación cancelada. Volviendo atrás...\n")
                    return
                else:
                    opcion=input("\nOpción inválida. Ingrese una opción válida (s/n): \n")
                    pass
            try:
                self.cursor.execute("INSERT INTO EDITORIALES (RUTEDIT, NOMEDIT, FONOEDI, CODPOSTEDI, REPRELEGEDI) VALUES (%s, %s, %s, %s, %s)"
                                    ,(rutedit, nombredit, fonoedit, codpostedit, represlegaldi))
                self.conexion.commit()
                print("\nEditorial agregada exitosamente.\n")
                break
            except Exception as e:
                print(f"Error al agregar editorial: {e}")
                self.conexion.rollback()

    # Función para mostrar una editorial
    def mostrar_editoriales(self):
        sql='select * from editoriales'
        try:
            self.cursor.execute(sql)
            lista=self.cursor.fetchall()
            lista_procesada = [[(campo if campo else "S/I") for campo in fila] for fila in lista]  
            print(tabulate(lista_procesada,headers=['Rut Edit.','Nombre','Teléfono','Cod. Postal','Representante Legal'],tablefmt='fancy_grid')) 
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
            print(f"\nNo se puede eliminar editorial {rutedit} porque tiene productos asociados.\n")
            return
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
editoriales.mostrar_editoriales()
editoriales.agregar_editorial()