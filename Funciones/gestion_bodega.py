import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import mysql.connector
from tabulate import tabulate
import re

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
        fono_bod = input("Ingrese el teléfono de la bodega: ")
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
            input("Precione cualquier tecla para continuar...")
        except Exception as e:
            print(f"Error al crear bodega: {e}")
            self.conexion.rollback()
        return cod_bod

    # Función para visualizar bodegas
    def mostrar_bodegas(self):
        sql='select * from bodegas'
        try:
            self.cursor.execute(sql)
            lista=self.cursor.fetchall()  
            print(tabulate(lista,headers=['Cod. Bod.','Sucursal','Teléfono','Jefe','Cod. Postal'],tablefmt='github'))    
        except Exception as err:
            print(err)

    # Función para eliminar una bodega  
    def eliminar_bodega(self):
        Bodegas().mostrar_bodegas()
        print("\n\n")
        cod_bod = input("Ingrese el código de la bodega a eliminar: ")
        self.cursor.execute("SELECT * FROM INVENTARIO WHERE CODBOD = %s", (cod_bod,))
        inventario = self.cursor.fetchone()

        if inventario:
            print("No se puede eliminar una bodega que contenga productos.")
        else:
            self.cursor.execute("DELETE FROM BODEGAS WHERE CODBOD = %s", (cod_bod,))
            self.conexion.commit()
            print("Bodega eliminada exitosamente.")
    
    def cerrarBD(self):
        self.cursor.close()
        self.conexion.close()

bodegas=Bodegas()
bodegas.eliminar_bodega()