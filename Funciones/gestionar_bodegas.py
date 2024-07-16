import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import mysql.connector
from tabulate import tabulate
import re
from os import system
from otras_funciones import validar_entero

class Bodegas():
    def __init__(self):
         self.conexion = mysql.connector.connect(
             host='localhost',
             user='root',
             password='inacap2023',
             database='elpoeta')
         self.cursor = self.conexion.cursor()

    # Función para crear una bodega 
    def crear_bodega(self,usuario):
        while True:
            print('-'*10+'Creación de Bodegas'+'-'*10+'\n')
            sucursal = input("Ingrese la sucursal: ").strip().upper()
            while sucursal=='':
                    sucursal = input("El nombre de la sucursal no puede estar vacío. Ingrese nuevamente: ").strip().upper()
            fono_bod = validar_entero("Ingrese el teléfono de la bodega: ",'teléfono')
            responsable = usuario
            self.cursor.execute("SELECT * FROM JEFEBODEGA WHERE RUNJEF = %s", (responsable,))
            jefe = self.cursor.fetchone()
            while not jefe:
                if responsable=='':
                    responsable=input("Entrada vacía. Ingrese un usuario válido (o 's' para finalizar): ").upper()
                elif responsable=='S':
                    system('cls')
                    print("\nOperación cancelada. Volviendo al menú de bodegas...\n")
                    return
                else:
                    responsable = input(f"Usuario {responsable} no existe. Ingrese un usuario válido (o 's' para finalizar): ").upper()
                self.cursor.execute("SELECT * FROM JEFEBODEGA WHERE RUNJEF = %s", (responsable,))
                jefe = self.cursor.fetchone()
            cod_post_bod = validar_entero("Ingrese el código postal de la bodega: ",'código postal')
            
            #aca para hacer el codigo de la bodega 
            consonantes = re.findall(r'[^NAEIOU\s]', sucursal)
            i_consonantes = ''.join(consonantes[:3]).upper()
            cont=1
            
            while True:
                cod_bod=f"{i_consonantes}{0}{cont}"
                self.cursor.execute("select * from bodegas where codbod=%s",(cod_bod,))
                resultado=self.cursor.fetchone()
                if not resultado:
                    break
                cont+=1
            bodega_nueva=[]
            bodega_nueva.append([cod_bod,sucursal,str(fono_bod),responsable,str(cod_post_bod)])
            print("\nSe creará la siguiente bodega:\n")
            print(tabulate(bodega_nueva,headers=['Cod. Bod.','Sucursal','Teléfono','Jefe','Cod. Postal'],tablefmt='fancy_grid')) 
            confirmar=input("\n¿Continuar? (s/n): ").lower()
            while confirmar not in ['s', 'n']:
                confirmar = input("\nOpción inválida. Ingrese una opción válida (s/n): ").lower()
            if confirmar=='s':
                try:
                    self.cursor.execute("INSERT INTO BODEGAS (CODBOD, SUCURSAL, FONOBOD, RESPONSABLE, CODPOSTBOD) VALUES (%s, %s, %s, %s, %s)",
                                    (cod_bod, sucursal, fono_bod, responsable, cod_post_bod))
                    self.conexion.commit()
                    system('cls')
                    print("\nBodega creada exitosamente.")
                    input("\nPresione ENTER para volver al menú de bodegas...")
                    system('cls')
                    return
                except Exception as e:
                    print(f"Error al crear bodega: {e}\n")
                    self.conexion.rollback()
                    return
            else:
                system('cls')
                input("\nOperación cancelada. Presione ENTER para volver atrás...")
                system('cls')
                return

    # Función para visualizar bodegas
    def mostrar_bodegas(self):
        print('-'*10+'Bodegas'+'-'*10+'\n')
        sql='select * from bodegas'
        try:
            self.cursor.execute(sql)
            lista=self.cursor.fetchall()
            lista_procesada = [[(campo if campo else "S/I") for campo in fila] for fila in lista]    
            print(tabulate(lista_procesada,headers=['Cod. Bod.','Sucursal','Teléfono','Jefe','Cod. Postal'],tablefmt='fancy_grid')) 
            print("\n")
        except Exception as e:
            print(f"Error al mostrar bodega: {e}\n")
            self.conexion.rollback()

    # Función para eliminar una bodega  
    def eliminar_bodega(self,usuario):
        print('-'*10+'Eliminar Bodegas'+'-'*10+'\n')
        Bodegas().mostrar_bodegas()
        while True:
            codbod = input("Ingrese el código de bodega a eliminar (o 's' para salir): ").upper()
            if codbod=='S':
                    system('cls')
                    print("\nVolviendo al menú de bodegas...\n")
                    return
            if codbod=='':
                    system('cls')
                    print('-'*10+'Eliminar Bodegas'+'-'*10+'\n')
                    Bodegas().mostrar_bodegas()
                    print("Entrada vacía. Reintente.\n")
                    continue
            self.cursor.execute("SELECT * FROM BODEGAS WHERE CODBOD = %s", (codbod,))
            bodega = self.cursor.fetchone()
            if not bodega:
                system('cls')
                print('-'*10+'Eliminar Bodegas'+'-'*10+'\n')
                Bodegas().mostrar_bodegas()
                print(f"Bodega {codbod} no existe. Reintente.\n")
                continue
            self.cursor.execute("SELECT RESPONSABLE FROM BODEGAS WHERE CODBOD = %s", (codbod,))
            jefe = self.cursor.fetchone()[0]
            if usuario!=jefe:
                system('cls')
                print(f'Usuario {usuario} no autorizado para eliminar bodega {codbod}. \nPor favor contacte al Jefe de Bodega correspondiente ({jefe}).\n')
                input('Presione ENTER para volver atrás...')
                system('cls')
                return
            self.cursor.execute("SELECT * FROM INVENTARIO WHERE BODEGA = %s", (codbod,))
            inventario = self.cursor.fetchone()
            if inventario:
                system('cls')
                print(f"\nNo se puede eliminar la bodega {codbod} porque contiene productos actualmente.\n")
                input('Presione ENTER para volver atrás...')
                system('cls')
                return
            else:
                system('cls')
                while True:
                    confirmar=input(f"¿Está seguro que desea eliminar la bodega {codbod}? (s/n): ").lower()
                    while confirmar not in ['s', 'n']:
                        confirmar = input("\nOpción inválida. Ingrese una opción válida (s/n): ").lower()
                    if confirmar == 's':
                        try:
                            self.cursor.execute("DELETE FROM BODEGAS WHERE CODBOD = %s", (codbod,))
                            self.conexion.commit()
                            system('cls')
                            Bodegas().mostrar_bodegas()
                            input("Bodega eliminada exitosamente. Presione ENTER para volver al menú de gestión de bodegas...")
                            system('cls')
                            return
                        except Exception as e:
                            print(f"Error al eliminar bodega: {e}")
                            self.conexion.rollback()
                    else:
                        system('cls')
                        input("Operación cancelada. Presione ENTER para volver al menú de gestión de bodegas...")
                        system('cls')
                        return 
    
    def cerrarBD(self):
        self.cursor.close()
        self.conexion.close()

