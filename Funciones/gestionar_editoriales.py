import sys
import os
from os import system
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
            print('-'*10+'Agregar Editoriales'+'-'*10+'\n')
            nombredit = input("Ingrese el nombre de la editorial: ").strip().upper()
            while nombredit=='':
                nombredit = input("El nombre de la editorial no puede estar vacío. Ingrese nuevamente: ").strip().upper()
            rutedit = input("Ingrese el RUT de la editorial: ").strip().upper()
            while rutedit=='':
                rutedit = input("El RUT de la editorial no puede estar vacío. Ingrese nuevamente: ").strip().upper()
            self.cursor.execute("SELECT * FROM EDITORIALES WHERE RUTEDIT = %s", (rutedit,))
            editorial = self.cursor.fetchone()
            if editorial:
                    print(f'\nLa editorial RUT {rutedit} ya se encuentra registrada en el sistema. \n\nIngrese una nueva editorial o vuelva atrás.')
                    opcion=input('\n¿Ingresar nueva editorial? (s/n): ')
                    if opcion=='s':
                        continue
                    elif opcion=='n':
                        system('cls')
                        print("\nOperación cancelada. Volviendo atrás...\n")
                        return
                    else:
                        opcion=input("\nOpción inválida. Ingrese una opción válida (s/n): \n")
                        pass
            fonoedit = validar_entero("Ingrese el teléfono de la editorial: ",'teléfono')
            codpostedit = validar_entero("Ingrese el código postal de la editorial: ",'código postal')
            represlegaldi = input("Ingrese el representante legal de la editorial: ").strip().upper()
            
            editorial_nueva=[]
            editorial_nueva.append([rutedit,nombredit,str(fonoedit),str(codpostedit),represlegaldi])
            print("\nSe creará la siguiente editorial:\n")
            print(tabulate(editorial_nueva,headers=['Rut Edit.','Nombre','Teléfono','Cod. Postal','Representante Legal'],tablefmt='fancy_grid')) 
            confirmar=input("\n¿Continuar? (s/n): ").lower()
            while confirmar not in ['s', 'n']:
                confirmar = input("\nOpción inválida. Ingrese una opción válida (s/n): ").lower()
            if confirmar=='s':
                try:
                    self.cursor.execute("INSERT INTO EDITORIALES (RUTEDIT, NOMEDIT, FONOEDI, CODPOSTEDI, REPRELEGEDI) VALUES (%s, %s, %s, %s, %s)"
                                        ,(rutedit, nombredit, fonoedit, codpostedit, represlegaldi))
                    self.conexion.commit()
                    print("\nEditorial creada exitosamente.")
                    input("\nPresione cualquier tecla para volver al menú de editoriales...")
                    system('cls')
                    return
                except Exception as e:
                    print(f"Error al agregar editorial: {e}")
                    self.conexion.rollback()
                    return
            else:
                system('cls')
                input("\nOperación cancelada. Presione cualquier tecla para volver atrás...\n")
                system('cls')
                return

    # Función para mostrar una editorial
    def mostrar_editoriales(self):
        print('-'*10+'Editoriales'+'-'*10+'\n')
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
        print('-'*10+'Eliminar Editoriales'+'-'*10+'\n')
        Editoriales().mostrar_editoriales()
        while True:
            rutedit = input("Ingrese el RUT de la editorial a eliminar (o 's' para salir): ").upper()
            self.cursor.execute("SELECT * FROM EDITORIALES WHERE rutedit = %s", (rutedit,))
            editoriales = self.cursor.fetchone()
            if rutedit=='S':
                system('cls')
                print("\nVolviendo al menú de editoriales...\n")
                return
            
            if not editoriales:
                if rutedit=='':
                    system('cls')
                    print('-'*10+'Eliminar Editoriales'+'-'*10+'\n')
                    Editoriales().mostrar_editoriales()
                    print("Entrada vacía. Reintente.\n")
                    continue
                else:
                    system('cls')
                    print('-'*10+'Eliminar Editoriales'+'-'*10+'\n')
                    Editoriales().mostrar_editoriales()
                    print(f"Editorial {rutedit} no existe. Reintente.\n")
                    continue
            self.cursor.execute("SELECT * FROM PRODUCTOS WHERE EDITORIAL = %s", (rutedit,))
            productos = self.cursor.fetchone()
            if productos:
                system('cls')
                print(f"\nNo se puede eliminar la editorial {rutedit} porque tiene productos asociados.\n")
                input('Presione cualquier tecla para volver atrás...')
                system('cls')
                return
            else:
                try:
                    self.cursor.execute("DELETE FROM EDITORIALES WHERE RUTEDIT = %s", (rutedit,))
                    self.conexion.commit()
                    system('cls')
                    Editoriales().mostrar_editoriales()
                    input("Editorial eliminada exitosamente. Presione cualquier tecla para volver al menú de editoriales...")
                    system('cls')
                    return
                except Exception as e:
                    print(f"Error al eliminar editorial: {e}")
                    self.conexion.rollback()

    def cerrarBD(self):
        self.cursor.close()
        self.conexion.close()

editoriales=Editoriales()
