import sys
import os
from os import system
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import mysql.connector
from tabulate import tabulate


from Funciones.gestionar_productos import Productos as p
from Funciones.gestionar_bodegas import Bodegas
from datetime import datetime
from Funciones.otras_funciones import ConexionBD

class Movimientos():

    def __init__(self):
        self.conexion = ConexionBD.conectar_db()
        if self.conexion:
            self.cursor = self.conexion.cursor()
    
    def mover_producto(self,user,locales):

        origen = Bodegas.cargar_bodegas(self,locales) 

        while not origen:
            nodata=print('No existen ni se han agregado bodegas con las que trabajar')
            input("\nPresione ENTER para volver al menú de productos...")                
            return



        print("Seleccione la bodega de origen:")
        for i, bodega in enumerate(origen, start=1):
            print(f"{i}. {bodega[1]} \t(COD: {origen[0]})")          

        bodega_origen = int(input("Ingrese el número correspondiente a la bodega: "))
        if bodega_origen < 1 or bodega_origen > len(origen):
            print("Opción no válida.")

        cod_origen = origen[bodega_origen - 1][0] 


        productos = p.cargar_productos(self)
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

        destino = Bodegas.cargar_bodegas(self,'') 

        print("Seleccione la bodega de destino:")
        for i, bodegad in enumerate(destino, start=1):
            print(f"{i}. {bodegad[1]} \t(COD: {destino[0]})")          

        bodega_destino = int(input("Ingrese el número correspondiente a la bodega: "))
        if bodega_destino < 1 or bodega_destino > len(destino):
            print("Opción no válida.")

        cod_destino = destino[bodega_destino - 1][0] 


        usuario=user


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


    def menu(self):
        while True:
            print("----- MENÚ DE INVENTARIO -----")
            print("1. Añadir producto a inventario")
            print("2. Mover producto entre inventarios")
            print("3. Salir")
            opcion = input("Ingrese una opción: ")

            if opcion == '1':
                self.añadir_productos()
            elif opcion == '2':
                self.mover_producto()
            elif opcion == '3':
                print("Saliendo del programa...")
                break
            else:
                print("Opción no válida. Intente nuevamente.")

            




mov=Movimientos()




