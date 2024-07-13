import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import mysql.connector
from tabulate import tabulate
import re
from os import system
from iniciar_sesion import *
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
    def crear_bodega(self):
        sucursal = input("Ingrese la sucursal: ").strip()
        while sucursal=='':
                sucursal = input("El nombre de la sucursal no puede estar vacío. Ingrese nuevamente: ").strip().upper()
        fono_bod = validar_entero("Ingrese el teléfono de la bodega: ",'teléfono')
        responsable = input("Ingrese el responsable: ").strip()
        cod_post_bod = validar_entero("Ingrese el código postal de la bodega: ",'código postal')
        
        #aca para hacer el codigo de la bodega 
        consonantes = re.findall(r'[^aeiounNAEIOU\s]', sucursal)
        i_consonantes = ''.join(consonantes[:3]).upper()
        cont=1
        self.cursor.execute("SELECT * FROM JEFEBODEGA WHERE RUNJEF = %s", (responsable,))
        jefe = self.cursor.fetchone()
        while not jefe:
            responsable = input(f"Usuario {responsable} no existe. Ingrese un usuario válido (o 's' para finalizar): ").upper()
            if responsable=='S':
                print("\nOperación cancelada.\n")
                return
            self.cursor.execute("SELECT * FROM JEFEBODEGA WHERE RUNJEF = %s", (responsable,))
            jefe = self.cursor.fetchone()
        while True:
            cod_bod=f"{i_consonantes}{0}{cont}"
            self.cursor.execute("select * from bodegas where codbod=%s",(cod_bod,))
            resultado=self.cursor.fetchone()
            if not resultado:
                break
            cont+=1
        try:
            self.cursor.execute("INSERT INTO BODEGAS (CODBOD, SUCURSAL, FONOBOD, RESPONSABLE, CODPOSTBOD) VALUES (%s, %s, %s, %s, %s)",
                            (cod_bod, sucursal, fono_bod, responsable, cod_post_bod))
            self.conexion.commit()
            print("Bodega creada exitosamente.")
            input("Presione cualquier tecla para continuar...")
            system('cls')
        except Exception as e:
            print(f"Error al crear bodega: {e}\n")
            self.conexion.rollback()
        return cod_bod

    # Función para visualizar bodegas
    def mostrar_bodegas(self):
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
    def eliminar_bodega(self):
        system('cls')
        Bodegas().mostrar_bodegas()
        print("\n")
        codbod = input("Ingrese el código de bodega a eliminar: ").upper()
        self.cursor.execute("SELECT * FROM INVENTARIO WHERE BODEGA = %s", (codbod,))
        inventario = self.cursor.fetchone()
        self.cursor.execute("SELECT * FROM BODEGAS WHERE CODBOD = %s", (codbod,))
        bodegas = self.cursor.fetchone()
        while not bodegas:
            while codbod=='':
                codbod = input("Entrada vacía. Ingrese un código de bodega a eliminar: ").strip().upper()
            codbod = input(f"Bodega {codbod} no existe. Ingrese el código de bodega nuevamente (o 's' para finalizar): ").upper()
            if codbod=='S':
                print("\nOperación cancelada.\n")
                return
            self.cursor.execute("SELECT * FROM BODEGAS WHERE CODBOD = %s", (codbod,))
            bodegas = self.cursor.fetchone()
        if inventario:
            print("\nNo se puede eliminar una bodega que contenga productos.\n")
        if bodegas['RESPONSABLE'] != self.usuario_actual:
            print("\nNo tiene permisos para eliminar esta bodega.\n")
            return
        else:
            try:
                self.cursor.execute("DELETE FROM BODEGAS WHERE CODBOD = %s", (codbod,))
                self.conexion.commit()
                print("\n")
                Bodegas().mostrar_bodegas()
                print("\nBodega eliminada exitosamente.\n")
            except Exception as e:
                print(f"Error al eliminar bodega: {e}")
                self.conexion.rollback()
    
    def cerrarBD(self):
        self.cursor.close()
        self.conexion.close()

bodegas=Bodegas()

bodegas.crear_bodega()
