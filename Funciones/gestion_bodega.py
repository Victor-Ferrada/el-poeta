import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import mysql.connector
from tabulate import tabulate
import re
from os import system

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
        sucursal = input("Ingrese la sucursal: ")
        fono_bod = input("Ingrese el teléfono de la bodega: ")            #indicar tipo int
        responsable = input("Ingrese el responsable: ")
        cod_post_bod = input("Ingrese el código postal de la bodega: ")
        
        #aca para hacer el codigo de la bodega 
        consonantes = re.findall(r'[^aeiounNAEIOU\s]', sucursal)
        i_consonantes = ''.join(consonantes[:3]).upper()
        cont=1
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
            print(tabulate(lista,headers=['Cod. Bod.','Sucursal','Teléfono','Jefe','Cod. Postal'],tablefmt='github')) 
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
            codbod = input(f"Bodega {codbod} no existe. Ingrese el código de bodega nuevamente (o 's' para finalizar): ").upper()
            if codbod=='S':
                print("\nOperación cancelada.\n")
                return
            self.cursor.execute("SELECT * FROM BODEGAS WHERE CODBOD = %s", (codbod,))
            bodegas = self.cursor.fetchone()
        if inventario:
            print("\nNo se puede eliminar una bodega que contenga productos.\n")
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

bodegas.eliminar_bodega()
