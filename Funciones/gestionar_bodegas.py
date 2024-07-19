import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tabulate import tabulate
import re
from os import system
from Funciones.otras_funciones import validar_entero,ConexionBD

class Bodegas():
    def __init__(self):
        self.conexion = ConexionBD.conectar_db()
        if self.conexion:
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
                    self.cursor.execute("insert into bodegas (codbod, sucursal, fonobod, responsable, codpostbod) values (%s, %s, %s, %s, %s)",
                                    (cod_bod, sucursal, fono_bod, responsable, cod_post_bod))
                    self.conexion.commit()
                    
                    system('cls')
                    print("\nBodega creada exitosamente.")
                    input("\nPresione ENTER para volver al menú de bodegas...")
                    system('cls')
                    
                    return i_consonantes
                except Exception as e:
                    print(f"Error al crear bodega: {e}\n")
                    self.conexion.rollback()
                    return None
            else:
                system('cls')
                input("\nOperación cancelada. Presione ENTER para volver atrás...")
                system('cls')
                return None

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
            try:
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
                self.cursor.execute("select * from bodegas where codbod = %s", (codbod,))
                bodega = self.cursor.fetchone()
                if not bodega:
                    system('cls')
                    print('-'*10+'Eliminar Bodegas'+'-'*10+'\n')
                    Bodegas().mostrar_bodegas()
                    print(f"Bodega {codbod} no existe. Reintente.\n")
                    continue
                self.cursor.execute("select responsable from bodegas where codbod = %s", (codbod,))
                jefe = self.cursor.fetchone()[0]
                if usuario!=jefe:
                    system('cls')
                    print(f'Usuario {usuario} no autorizado para eliminar bodega {codbod}. \nPor favor contacte al Jefe de Bodega correspondiente ({jefe}).\n')
                    input('Presione ENTER para volver atrás...')
                    system('cls')
                    return
                self.cursor.execute("select * from movimientos where bodega = %s", (codbod,))
                movimientos = self.cursor.fetchone()
                
                if movimientos:
                    system('cls')
                    print(f"\nNo se puede eliminar la bodega {codbod} porque tiene movimientos registrados.\n")
                    input('Presione ENTER para volver atrás...')
                    system('cls')
                    print('-'*10 + 'Eliminar Bodegas' + '-'*10 + '\n')
                    Bodegas().mostrar_bodegas()
                    continue
                self.cursor.execute("select * from inventario where bodega = %s and stock>0", (codbod,))
                inventario = self.cursor.fetchone()
                if inventario:
                    system('cls')
                    print(f"\nNo se puede eliminar la bodega {codbod} porque contiene productos actualmente.\n")
                    input('Presione ENTER para volver atrás...')
                    system('cls')
                    print('-'*10+'Eliminar Bodegas'+'-'*10+'\n')
                    Bodegas().mostrar_bodegas()
                    continue
                system('cls')
                self.cursor.execute("select * from inventario where bodega = %s and stock=0", (codbod,))
                inventario2 = self.cursor.fetchone()
                confirmar=input(f"¿Está seguro que desea eliminar la bodega {codbod}? (s/n): ").lower()
                
                while confirmar not in ['s', 'n']:
                    confirmar = input("\nOpción inválida. Ingrese una opción válida (s/n): ").lower()
                if confirmar == 's':
                    try:
                        if inventario2:
                            self.cursor.execute("delete from inventario where bodega=%s",(codbod,))
                            self.conexion.commit()
                        self.cursor.execute("delete from bodegas where codbod = %s", (codbod,))
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
            except Exception as e:
                print(f"Error inesperado: {e}")
                self.conexion.rollback()
    
    def cargar_bodegas(self,locales):
        try:
            sql_bodegas = f"select codbod, sucursal from bodegas where codbod like '{locales}%'"
            self.cursor.execute(sql_bodegas)
            bodegas = self.cursor.fetchall()
            return bodegas
        except Exception as e:
            print(f"Error al cargar bodegas: {e}")
            return []

