import sys
import os
from os import system
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tabulate import tabulate


from gestionar_productos import Productos as p
from gestionar_bodegas import Bodegas
from datetime import datetime
from otras_funciones import ConexionBD

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
        for i, bodegao in enumerate(origen, start=1):
            print(f"{i}. {bodegao[1]} \t(COD: {bodegao[0]})")          

        bodega_origen = int(input("Ingrese el número correspondiente a la bodega: "))
        if bodega_origen < 1 or bodega_origen > len(origen):
            print("Opción no válida.")

        cod_origen = origen[bodega_origen - 1][0] 


        productos = p.cargar_productos(self)
        while not productos:
            nodata=print('No existen ni se han agregado productos con las que trabajar')
            input("\nPresione ENTER para volver al menú de productos...")                
            return         


        query = " SELECT p.codProd, p.nomProd, i.stock FROM Productos p JOIN Inventario i ON p.codProd = i.codProd WHERE i.bodega = %s;"
        self.cursor.execute(query,(cod_origen,))
        productos_filtrados = self.cursor.fetchall()

        if not productos_filtrados:
            print("No hay productos disponibles en la bodega de origen.")
            return

        print("Seleccione los productos a mover (ingrese 0 para terminar):")
        productos_a_mover = []
        while True:
            print("\nProductos disponibles:")
            for i, producto in enumerate(productos_filtrados, start=1):
                stock_producto = producto[2] if producto[2] is not None else 0
                print(f"{i}. {producto[1]} \t(COD: {producto[0]}) \tStock: {stock_producto}")

            producto_mover = int(input("Ingrese el número correspondiente al producto (0 para terminar): "))
            if producto_mover == 0:
                break
            elif producto_mover < 1 or producto_mover > len(productos_filtrados):
                print("Opción no válida.")
                continue

            cod_prod = productos_filtrados[producto_mover - 1][0]
            stock_disponible = productos_filtrados[producto_mover - 1][2] if productos_filtrados[producto_mover - 1][2] is not None else 0

            stock = int(input("Ingrese el stock del producto: "))
            while stock == '':
                stock = int(input("El stock del producto no puede estar vacío. Ingrese nuevamente: "))
            if stock > stock_disponible:
                print(f"Error: El stock solicitado ({stock}) excede el stock disponible en la bodega de origen ({stock_disponible}).")
                continue            

            productos_a_mover.append((cod_prod, stock))

        if not productos_a_mover:
            print("No se seleccionaron productos para mover.")
            return

        destino = Bodegas.cargar_bodegas(self,'') 

        print("Seleccione la bodega de destino:")
        for i, bodegad in enumerate(destino, start=1):
            print(f"{i}. {bodegad[1]} \t(COD: {bodegad[0]})")          

        bodega_destino = int(input("Ingrese el número correspondiente a la bodega: "))
        if bodega_destino < 1 or bodega_destino > len(destino):
            print("Opción no válida.")

        cod_destino = destino[bodega_destino - 1][0] 

        if cod_origen == cod_destino:
            print("Error: La bodega de destino no puede ser la misma que la bodega de origen.")
            return


        usuario=user


        try:
            query_verificar_producto = "SELECT * FROM Inventario WHERE codProd = %s AND bodega = %s"
            self.cursor.execute(query_verificar_producto, (cod_prod, cod_destino))
            producto_existente = self.cursor.fetchone()
            if not producto_existente:
                sql_last_id_inv = "SELECT MAX(codIng) FROM inventario"
                self.cursor.execute(sql_last_id_inv)
                last_cod_inv = self.cursor.fetchone()[0]
                if last_cod_inv is None:
                    last_cod_inv = 0
                last_cod_inv = int(last_cod_inv)
                codinv = last_cod_inv + 1     

                sql_agregar_producto = "INSERT INTO Inventario (codIng, codProd, bodega, stock) VALUES (%s, %s, %s, 0)"
                self.cursor.execute(sql_agregar_producto, (codinv, cod_prod, cod_destino))            
            
            sql_last_id_mov = "SELECT MAX(codMov) FROM movimientos"
            self.cursor.execute(sql_last_id_mov)
            last_cod_mov = self.cursor.fetchone()[0]

            if last_cod_mov is None:
                last_cod_mov = 0
            last_cod_mov = int(last_cod_mov)
            codmovd = last_cod_mov + 1

            fechamov = datetime.now()   


            for cod_prod, stock in productos_a_mover:
                # Insertar el movimiento de despacho
                sql_movimiento_despacho = "INSERT INTO Movimientos (codMov, codProd, tipoMov, fechaMov, stock, bodega, usuario) VALUES (%s, %s, 'DESPACHO', %s, %s, %s, %s)"
                self.cursor.execute(sql_movimiento_despacho, (codmovd, cod_prod, fechamov, stock, cod_origen, usuario))

                codmovr= codmovd+1

                # Insertar el movimiento de recepción
                sql_movimiento_recepcion = "INSERT INTO Movimientos (codMov, codProd, tipoMov, fechaMov, stock, bodega, usuario) VALUES (%s, %s, 'RECEPCION', %s, %s, %s, %s)"
                self.cursor.execute(sql_movimiento_recepcion, (codmovr, cod_prod, fechamov, stock, cod_destino, usuario))

                # Actualizar el inventario de la bodega de origen
                sql_inventario_despacho = "UPDATE Inventario SET stock = stock - %s WHERE bodega = %s AND codProd = %s"
                self.cursor.execute(sql_inventario_despacho, (stock, cod_origen, cod_prod))

                # Verificar si el producto está registrado en la bodega de destino
                query_verificar_producto = "SELECT * FROM Inventario WHERE codProd = %s AND bodega = %s"
                self.cursor.execute(query_verificar_producto, (cod_prod, cod_destino))
                producto_existente = self.cursor.fetchone()

                if not producto_existente:
                    sql_last_id_inv = "SELECT MAX(codIng) FROM inventario"
                    self.cursor.execute(sql_last_id_inv)
                    last_cod_inv = self.cursor.fetchone()[0]
                    if last_cod_inv is None:
                        last_cod_inv = 0
                    last_cod_inv = int(last_cod_inv)
                    codinv = last_cod_inv + 1     

                    sql_agregar_producto = "INSERT INTO Inventario (codIng, codProd, bodega, stock) VALUES (%s, %s, %s, 0)"
                    self.cursor.execute(sql_agregar_producto, (codinv, cod_prod, cod_destino))   
                else:
                    # Actualizar el inventario de la bodega de destino
                    sql_inventario_recepcion = "UPDATE Inventario SET stock = stock + %s WHERE bodega = %s AND codProd = %s"
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
                self.mover_producto('12345678-9','THN')
            elif opcion == '3':
                print("Saliendo del programa...")
                break
            else:
                print("Opción no válida. Intente nuevamente.")

            




mov=Movimientos()
mov.menu()


