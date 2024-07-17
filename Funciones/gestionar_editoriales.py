import sys
import os
from os import system
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tabulate import tabulate
from Funciones.otras_funciones import validar_entero,ConexionBD

class Editoriales():
    def __init__(self):
        self.conexion = ConexionBD.conectar_db()
        if self.conexion:
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
            self.cursor.execute("select * from editoriales where rutedit = %s", (rutedit,))
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
            print("\nSe agregará la siguiente editorial:\n")
            print(tabulate(editorial_nueva,headers=['RUT','Nombre','Teléfono','Cod. Postal','Representante Legal'],tablefmt='fancy_grid')) 
            confirmar=input("\n¿Continuar? (s/n): ").lower()
            while confirmar not in ['s', 'n']:
                confirmar = input("\nOpción inválida. Ingrese una opción válida (s/n): ").lower()
            if confirmar=='s':
                try:
                    self.cursor.execute("insert into editoriales (rutedit, nomedit, fonoedi, codpostedi, reprelegedi) values (%s, %s, %s, %s, %s)"
                                        ,(rutedit, nombredit, fonoedit, codpostedit, represlegaldi))
                    self.conexion.commit()
                    system('cls')
                    print("\nEditorial agregada exitosamente.")
                    input("\nPresione ENTER para volver atrás...")
                    system('cls')
                    return
                except Exception as e:
                    print(f"Error al agregar editorial: {e}")
                    self.conexion.rollback()
                    return
            else:
                system('cls')
                input("\nOperación cancelada. Presione ENTER para volver atrás...")
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
            print(tabulate(lista_procesada,headers=['RUT','Nombre','Teléfono','Cod. Postal','Representante Legal'],tablefmt='fancy_grid')) 
            print("\n")
        except Exception as e:
            print(f"Error al mostrar editoriales: {e}")
            self.conexion.rollback()

    # Función para eliminar una editorial
    def eliminar_editorial(self,usuario):
        print('-'*10+'Eliminar Editoriales'+'-'*10+'\n')
        Editoriales().mostrar_editoriales()
        while True:
            try:
                rutedit = input("Ingrese el RUT de la editorial a eliminar (o 's' para salir): ").upper()
                if rutedit=='S':
                    system('cls')
                    print("\nVolviendo al menú de editoriales...\n")
                    return
                if rutedit=='':
                        system('cls')
                        print('-'*10+'Eliminar Editoriales'+'-'*10+'\n')
                        Editoriales().mostrar_editoriales()
                        print("Entrada vacía. Reintente.\n")
                        continue
                self.cursor.execute("select * from editoriales where rutedit = %s", (rutedit,))
                editorial = self.cursor.fetchone()
                if not editorial:
                    system('cls')
                    print('-'*10+'Eliminar Editoriales'+'-'*10+'\n')
                    Editoriales().mostrar_editoriales()
                    print(f"Editorial {rutedit} no existe. Reintente.\n")
                    continue
                self.cursor.execute("select runjef from jefebodega")
                jefes=self.cursor.fetchall()
                jefes=[jefe[0] for jefe in jefes]
                if usuario not in jefes:
                    system('cls')
                    print(f'Usuario {usuario} no autorizado para eliminar editorial {rutedit}. Por favor contacte al Jefe de Bodega.\n')
                    input('Presione ENTER para volver atrás...')
                    system('cls')
                    return
                self.cursor.execute("select * from productos where editorial = %s", (rutedit,))
                productos = self.cursor.fetchone()
                if productos:
                    system('cls')
                    print(f"\nNo se puede eliminar la editorial {rutedit} porque tiene productos asociados.\n")
                    input('Presione ENTER para volver atrás...')
                    system('cls')
                    print('-'*10+'Eliminar Editoriales'+'-'*10+'\n')
                    Editoriales().mostrar_editoriales()
                    continue
                confirmar = input(f"¿Está seguro que desea eliminar la editorial {rutedit}? (s/n): ").lower()
                        
                while confirmar not in ['s', 'n']:
                    confirmar = input("\nOpción inválida. Ingrese una opción válida (s/n): ").lower()
            
                if confirmar == 's':
                    try:
                        self.cursor.execute("delete from editoriales where rutedit = %s", (rutedit,))
                        self.conexion.commit()
                        system('cls')
                        Editoriales().mostrar_editoriales()
                        input("Editorial eliminada exitosamente. Presione ENTER para volver al menú de editoriales...")
                        system('cls')
                        return
                    except Exception as e:
                        print(f"Error al eliminar editorial: {e}")
                        self.conexion.rollback()
                else:
                    system('cls')
                    input("Operación cancelada. Presione ENTER para volver al menú de editoriales...")
                    system('cls')
                    return 
            except Exception as e:
                print(f"Error inesperado: {e}")
                self.conexion.rollback()

    def cargar_editoriales(self):
        try:
            sql_editoriales = "select rutedit, nomedit from editoriales"
            self.cursor.execute(sql_editoriales)
            editoriales = self.cursor.fetchall()
            return editoriales
        except Exception as e:
            print(f"Error al cargar editoriales: {e}")
            return []


editoriales=Editoriales()
