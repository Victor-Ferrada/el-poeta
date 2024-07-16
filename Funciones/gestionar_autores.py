import sys
import os
from os import system
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import mysql.connector
from tabulate import tabulate
from Funciones.otras_funciones import validar_entero

class Autores():
    def __init__(self):
         self.conexion = mysql.connector.connect(
             host='localhost',
             user='root',
             password='inacap2023',
             database='elpoeta')
         self.cursor = self.conexion.cursor()
    
    def cargar_autores(self):
        try:
            sql_autores = "SELECT runautor, nombresau, appatau FROM autores"
            self.cursor.execute(sql_autores)
            autores = self.cursor.fetchall()
            return autores
        except Exception as e:
            print(f"Error al cargar autores: {e}")
            return []


    # Función para agregar un autor
    def agregar_autor(self):
        while True:
            print('-'*10+'Agregar Autores'+'-'*10+'\n')
            nombraut = input("Ingrese el nombre del autor: ").strip().upper()
            while nombraut=='':
                nombraut = input("El nombre del autor no puede estar vacío. Ingrese nuevamente: ").strip().upper()
            appataut = input("Ingrese el apellido paterno del autor: ").strip().upper()
            while nombraut=='':
                nombraut = input("El apellido paterno del autor no puede estar vacío. Ingrese nuevamente: ").strip().upper()
            apmataut = input("Ingrese el apellido materno del autor: ").strip().upper()
            while nombraut=='':
                nombraut = input("El apellido materno del autor no puede estar vacío. Ingrese nuevamente: ").strip().upper()                            
            runaut = input("Ingrese el RUN del autor: ").strip().upper()
            while runaut=='':
                runaut = input("El RUN del autor no puede estar vacío. Ingrese nuevamente: ").strip().upper()
            self.cursor.execute("SELECT * FROM AUTORES WHERE RUNAUTOR = %s", (runaut,))
            autor = self.cursor.fetchone()
            if autor:
                    print(f'\nEl autor RUN {runaut} ya se encuentra registrado en el sistema. \n\nIngrese un nuevo autor o vuelva atrás.')
                    opcion=input('\n¿Ingresar nuevo autor? (s/n): ')
                    if opcion=='s':
                        system('cls')
                        continue
                    elif opcion=='n':
                        system('cls')
                        print("\nOperación cancelada. Volviendo atrás...\n")
                        return
                    else:
                        opcion=input("\nOpción inválida. Ingrese una opción válida (s/n): \n")
                        pass
            fonoau = validar_entero("Ingrese el teléfono del autor: ",'teléfono')
            codpostaut = validar_entero("Ingrese el código postal del autor: ",'código postal')
            
            autor_nuevo=[]
            autor_nuevo.append([runaut,nombraut,appataut,apmataut,str(fonoau),str(codpostaut)])
            print("\nSe agregará el siguiente autor:\n")
            print(tabulate(autor_nuevo,headers=['RUN','Nombre','Apellido paterno','Apellido materno','Teléfono','Cod. Postal'],tablefmt='fancy_grid')) 
            confirmar=input("\n¿Continuar? (s/n): ").lower()
            while confirmar not in ['s', 'n']:
                confirmar = input("\nOpción inválida. Ingrese una opción válida (s/n): ").lower()
            if confirmar=='s':
                try:
                    self.cursor.execute("INSERT INTO AUTORES (RUNAUTOR, NOMBRESAU, APPATAU, APMATAU, FONOAU, CODPOSTAU) VALUES (%s, %s, %s, %s, %s, %s)"
                                        ,(runaut, nombraut, appataut, apmataut, fonoau, codpostaut))
                    self.conexion.commit()
                    system('cls')
                    print("\nAutor agregado exitosamente.")
                    input("\nPresione ENTER para volver al menú de autores...")
                    system('cls')
                    return
                except Exception as e:
                    print(f"Error al agregar autor: {e}")
                    self.conexion.rollback()
                    return
            else:
                system('cls')
                input("\nOperación cancelada. Presione ENTER para volver atrás...")
                system('cls')
                return

    # Función para mostrar un autor
    def mostrar_autores(self):
        print('-'*10+'Autores'+'-'*10+'\n')
        sql='select * from autores'
        try:
            self.cursor.execute(sql)
            lista=self.cursor.fetchall()
            lista_procesada = [[(campo if campo else "S/I") for campo in fila] for fila in lista]  
            print(tabulate(lista_procesada,headers=['RUT','Nombre','Apellido paterno','Apellido materno','Teléfono','Cod. Postal'],tablefmt='fancy_grid')) 
            print("\n")
        except Exception as e:
            print(f"Error al mostrar autores: {e}")
            self.conexion.rollback()

    # Función para eliminar un autor
    def eliminar_autor(self,usuario):
        print('-'*10+'Eliminar Autores'+'-'*10+'\n')
        Autores().mostrar_autores()
        while True:
            runaut = input("Ingrese el RUN del autor a eliminar (o 's' para salir): ").upper()
            if runaut=='S':
                system('cls')
                print("\nVolviendo al menú de autores...\n")
                return
            if runaut=='':
                    system('cls')
                    print('-'*10+'Eliminar Autores'+'-'*10+'\n')
                    Autores().mostrar_autores()
                    print("Entrada vacía. Reintente.\n")
                    continue
            self.cursor.execute("SELECT * FROM AUTORES WHERE RUNAUTOR = %s", (runaut,))
            autor = self.cursor.fetchone()
            if not autor:
                system('cls')
                print('-'*10+'Eliminar Autores'+'-'*10+'\n')
                Autores().mostrar_autores()
                print(f"Autor {runaut} no existe. Reintente.\n")
                continue
            self.cursor.execute("SELECT RUNJEF FROM JEFEBODEGA")
            jefes=self.cursor.fetchall()
            jefes=[jefe[0] for jefe in jefes]
            if usuario not in jefes:
                system('cls')
                print(f'Usuario {usuario} no autorizado para eliminar autor {runaut}. Por favor contacte al Jefe de Bodega.\n')
                input('Presione ENTER para volver atrás...')
                system('cls')
                return
            self.cursor.execute("SELECT * FROM AUPROD WHERE RUNAUTOR = %s", (runaut,))
            productos = self.cursor.fetchone()
            if productos:
                system('cls')
                print(f"\nNo se puede eliminar el autor {runaut} porque tiene productos asociados.\n")
                input('Presione ENTER para volver atrás...')
                system('cls')
                return
            else:
                system('cls')
                while True:
                    confirmar=input(f"¿Está seguro que desea eliminar el autor {runaut}? (s/n): ").lower()
                    while confirmar not in ['s', 'n']:
                        confirmar = input("\nOpción inválida. Ingrese una opción válida (s/n): ").lower()
                    if confirmar == 's':
                        try:
                            self.cursor.execute("DELETE FROM AUTORES WHERE RUNAUTOR = %s", (runaut,))
                            self.conexion.commit()
                            system('cls')
                            Autores().mostrar_autores()
                            input("Autor eliminado exitosamente. Presione ENTER para volver al menú de autores...")
                            system('cls')
                            return
                        except Exception as e:
                            print(f"Error al eliminar autor: {e}")
                            self.conexion.rollback()
                    else:
                        system('cls')
                        input("Operación cancelada. Presione ENTER para volver al menú de autores...")
                        system('cls')
                        return 

    def cerrarBD(self):
        self.cursor.close()
        self.conexion.close()

au=Autores()