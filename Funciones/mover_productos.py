import sys
import os
from os import system
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import mysql.connector
from tabulate import tabulate

from gestionar_editoriales import Editoriales
from gestionar_autores import Autores
from gestionar_productos import Productos
from gestionar_bodegas import Bodegas
from datetime import datetime

class Inventario():

    def __init__(self):
        self.conexion = mysql.connector.connect(
            host='localhost',
            user='root',
            password='12345678',
            database='elpoeta')
        self.cursor = self.conexion.cursor()
    

# Función para mover productos 
    def añadir_productos(self):


        productos = Productos.cargar_productos(self)
            
        while not productos:
            nodata=print('No existen ni se han agregado productos con los que trabajar')
            input("\nPresione ENTER para volver al menú de productos...")
            return
        

        print("Seleccione la el producto a inventariar:")
        for i, producto in enumerate(productos, start=1):
            print(f"{i}. {producto[1]} \t(COD: {productos[0]})")          

        opcion_producto = int(input("Ingrese el número correspondiente al producto: "))
        if opcion_producto < 1 or opcion_producto > len(productos):
            print("Opción no válida.")

        cod_prod = productos[opcion_producto - 1][0]


        bodegas = Bodegas.cargar_bodegas(self) 

        while not bodegas:
            nodata=print('No existen ni se han agregado bodegas con las que trabajar')
            input("\nPresione ENTER para volver al menú de productos...")                
            return



        print("Seleccione la bodega del producto:")
        for i, bodega in enumerate(bodegas, start=1):
            print(f"{i}. {bodega[1]} \t(COD: {bodegas[0]})")          

        opcion_bodega = int(input("Ingrese el número correspondiente a la bodega: "))
        if opcion_bodega < 1 or opcion_bodega > len(bodegas):
            print("Opción no válida.")

        cod_bodega = bodegas[opcion_bodega - 1][0]


        stock = int(input("Ingrese el stock del producto: "))
        while stock=='':
            stock = int(input("El stock del producto no puede estar vacío. Ingrese nuevamente: "))

        try:
            sql_last_id_inv = "SELECT MAX(codIng) FROM inventario"
            self.cursor.execute(sql_last_id_inv)
            last_cod_inv = self.cursor.fetchone()[0]

            if last_cod_inv is None:
                last_cod_inv = 0
            last_cod_inv = int(last_cod_inv)
            codinv = last_cod_inv + 1            
            
            sql_insertar_producto = "INSERT INTO Inventario (codIng, codProd, bodega, stock) VALUES (%s, %s, %s, %s)"
            self.cursor.execute(sql_insertar_producto, (codinv, cod_prod, cod_bodega, stock))
                    
            self.conexion.commit()
            print("\nProducto agregado exitosamente.\n")            

        except ValueError:
            print("Ingrese un número válido para seleccionar la editorial, el autor o el tipo de producto.")
        except Exception as e:
            print(f"Error al agregar producto: {e}")
            self.conexion.rollback()


    def mover_producto(self):

        bodegas = Bodegas.cargar_bodegas(self) 

        while not bodegas:
            nodata=print('No existen ni se han agregado bodegas con las que trabajar')
            input("\nPresione ENTER para volver al menú de productos...")                
            return



        print("Seleccione la bodega de origen:")
        for i, bodega in enumerate(bodegas, start=1):
            print(f"{i}. {bodega[1]} \t(COD: {bodegas[0]})")          

        bodega_origen = int(input("Ingrese el número correspondiente a la bodega: "))
        if bodega_origen < 1 or bodega_origen > len(bodegas):
            print("Opción no válida.")

        cod_origen = bodegas[bodega_origen - 1][0] 


        productos = Productos.cargar_productos(self)
        while not productos:
            nodata=print('No existen ni se han agregado productos con las que trabajar')
            input("\nPresione ENTER para volver al menú de productos...")                
            return         


        query =  "SELECT p.nomProd, i.codProd FROM Productos p JOIN Inventario i ON p.codProd = i.codProd WHERE i.bodega = %s "
        self.cursor.execute("SELECT p.nomProd, i.codProd FROM Productos p JOIN Inventario i ON p.codProd = i.codProd WHERE i.bodega = %s ",(cod_origen,))
        productos_filtrados = self.cursor.fetchall()



        print("Seleccione el producto a mover:")
        for i, producto in enumerate(productos_filtrados, start=1):
            print(f"{i}. {producto[1]} \t(COD: {productos_filtrados[0]})")          

        producto_mover= int(input("Ingrese el número correspondiente al producto: "))
        if producto_mover < 1 or producto_mover > len(productos_filtrados):
            print("Opción no válida.")

        cod_prod = productos_filtrados[producto_mover - 1][0]
        
        stock = int(input("Ingrese el stock del producto: "))
        while stock=='':
            stock = int(input("El stock del producto no puede estar vacío. Ingrese nuevamente: "))


        print("Seleccione la bodega de destino:")
        for i, bodegad in enumerate(bodegas, start=1):
            print(f"{i}. {bodegad[1]} \t(COD: {bodegas[0]})")          

        bodega_destino = int(input("Ingrese el número correspondiente a la bodega: "))
        if bodega_destino < 1 or bodega_destino > len(bodegas):
            print("Opción no válida.")

        cod_destino = bodegas[bodega_destino - 1][0] 


        usuario= input('rut bodeguero:')#ajustar con usuario logeado








        try:
            sql_last_id_mov = "SELECT MAX(codMov) FROM movimientos"
            self.cursor.execute(sql_last_id_mov)
            last_cod_mov = self.cursor.fetchone()[0]

            if last_cod_mov is None:
                last_cod_mov = 0
            last_cod_mov = int(last_cod_mov)
            codmovd = last_cod_mov + 1

            fechamov = datetime.now()            
            
            sql_movimiento_despacho = "INSERT INTO Movimientos (codMov, codProd, tipoMov, fechaMov, stock, bodega, usuario) VALUES (%s, %s, 'DESPACHO', %s, %s, %s, %s)"
            self.cursor.execute(sql_movimiento_despacho, (codmovd, cod_prod, fechamov, stock, cod_origen, usuario))

            codmovr= codmovd+1

            sql_movimiento_recepcion = "INSERT INTO Movimientos (codMov, codProd, tipoMov, fechaMov, stock, bodega, usuario) VALUES (%s, %s, 'RECEPCION', %s, %s, %s, %s)"
            self.cursor.execute(sql_movimiento_recepcion, (codmovr, cod_prod, fechamov, stock, cod_destino, usuario))

            sql_inventario_despacho = "UPDATE inventario SET stock = stock - %s WHERE bodega = %s AND codProd = %s"
            self.cursor.execute(sql_inventario_despacho, (stock, cod_origen, cod_prod))            

            sql_inventario_recepcion = "UPDATE inventario SET stock = stock + %s WHERE bodega = %s AND codProd = %s"
            self.cursor.execute(sql_inventario_recepcion, (stock, cod_destino, cod_prod))                        

            self.conexion.commit()
            print("\nProducto agregado exitosamente.\n")            

        except ValueError:
            print("Ingrese un número válido para seleccionar la editorial, el autor o el tipo de producto.")
        except Exception as e:
            print(f"Error al agregar producto: {e}")
            self.conexion.rollback()
