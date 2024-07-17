import sys
import os
from os import system
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tabulate import tabulate


from Funciones.gestionar_productos import Productos as p
from Funciones.gestionar_bodegas import Bodegas
from datetime import datetime
from Funciones.otras_funciones import ConexionBD,validar_entero

class Movimientos():

    def __init__(self):
        self.conexion = ConexionBD.conectar_db()
        if self.conexion:
            self.cursor = self.conexion.cursor()
    
    def mover_producto(self, user, locales):
            try:
                # Cargar las bodegas de origen       
                origen = Bodegas.cargar_bodegas(self, locales)


                while True:
                    if not origen:
                        system('cls')
                        print('No existen ni se han agregado bodegas con las que trabajar.')
                        input("\nPresione ENTER para volver atrás ...")
                        system('cls')
                        return

                    print("Seleccione la bodega de origen:")
                    bodegas_origen = [[i, bodega[1], bodega[0]] for i, bodega in enumerate(origen, start=1)]
                    print(tabulate(bodegas_origen, headers=['Nº', 'Nombre', 'Código'], tablefmt='fancy_grid'))

                    bodega_origen = input("Ingrese el número correspondiente a la bodega de origen (0 para cancelar): ")
                    if not bodega_origen.isdigit():
                        system('cls')
                        print("Por favor, ingrese un número.")
                        continue

                    bodega_origen = int(bodega_origen)

                    if bodega_origen == 0:
                        system('cls')
                        input("\nPresione ENTER para volver atrás ...")
                        system('cls')
                        return  

                    if bodega_origen < 1 or bodega_origen > len(origen):
                        system('cls')
                        print(f"Opción no válida, debe ser un número entre 1 y {len(origen)}.")
                    else:
                        cod_origen = origen[bodega_origen - 1][0]
                        break  # Salir del bucle si la opción es válida




                productos = p.cargar_productos(self)
                while not productos:
                    system('cls')
                    print('No existen ni se han agregado productos con las que trabajar.')
                    input("\nPresione ENTER para volver atrás ...")
                    system('cls')                
                    return         


                query = " select p.codprod, p.nomprod, i.stock from productos p join inventario i on p.codprod = i.codprod where i.bodega = %s;"
                self.cursor.execute(query,(cod_origen,))
                productos_filtrados = self.cursor.fetchall()

                if not productos_filtrados:
                    system('cls')
                    print("No hay productos disponibles en la bodega de origen.")
                    input("\nPresione ENTER para volver atrás ...") 
                    system('cls')
                    return
                
                system('cls')

                print("Seleccione los productos a mover.")
                while True:
                    productos_a_mover = []
                    productos_seleccionados = []
                    mover_otro = 's'
                    
                    while mover_otro.lower() == 's':
                        
                        print("Productos disponibles en bodega:")
                        productosi = []
                        for i, producto in enumerate(productos_filtrados, start=1):
                            stock_producto = producto[2] if producto[2] is not None else 0
                            productosi.append([i, producto[1], producto[0], stock_producto])

                        print(tabulate(productosi, headers=['Nº', 'Nombre', 'Código', 'Stock'], tablefmt='fancy_grid'))  

                        producto_mover = input("Ingrese el número correspondiente al producto(0 para cancelar): ")
                        
                        
                        if not producto_mover.isdigit():
                            system('cls')
                            print("Por favor, ingrese un número.")
                            continue
                        
                        producto_mover = int(producto_mover)

                        if producto_mover == 0:
                            input("\nPresione ENTER para volver atrás ...")
                            system('cls')
                            return
                        if producto_mover < 1 or producto_mover > len(productos_filtrados):
                            system('cls')
                            print(f"Opción no válida, debe ser un número entre 1 y {len(productos_filtrados)}.")
                            continue
                        
                        cod_prod = productos_filtrados[producto_mover - 1][0]

                        if cod_prod in productos_seleccionados:
                            system('cls')
                            print("Error: Este producto ya ha sido seleccionado.")
                            continue


                        stock_disponible = productos_filtrados[producto_mover - 1][2] if productos_filtrados[producto_mover - 1][2] is not None else 0 

                        while True:
                            try:
                                stock = int(input(f"Ingrese el stock del producto (0 para cancelar) '{productos_filtrados[producto_mover - 1][1]}': "))
                                if stock < 0:
                                    print("El stock del producto debe ser mayor que cero.")
                                    continue
                                if stock == 0:
                                    input("\nPresione ENTER para volver atrás ...")
                                    system('cls')
                                    return 
                                if stock > stock_disponible:
                                    print(f"Error: El stock solicitado ({stock}) excede el stock disponible en la bodega de origen ({stock_disponible}).")
                                    continue
                                break
                            except ValueError:
                                print("Por favor, ingrese un número entero válido para el stock.")
                                continue  

                        productos_a_mover.append((cod_prod, stock))
                        productos_seleccionados.append(cod_prod)
                        mover_otro = input("¿Desea mover otro producto? (s/n): ").strip().lower()
                        
                        while mover_otro not in ['s', 'n']:
                            system('cls')
                            print("Respuesta no válida. Por favor ingrese 's' para agregar otro autor o 'n' para terminar.")
                            mover_otro = input("¿Desea agregar otro autor? (s/n): ").strip().lower()

                        system('cls')
                    
                    if not productos_seleccionados:
                        print("Debe seleccionar al menos un producto.")
                        continue
                    
                    break

                # Cargar las bodegas de destino
                destino = Bodegas.cargar_bodegas(self, '')


                system('cls')


                while True:
                    if not destino:
                        print('No existen ni se han agregado bodegas con las que trabajar.')
                        input("\nPresione ENTER para volver atrás ...")
                        system('cls')
                        return

                    print("Seleccione la bodega de destino:")
                    bodegas_destino = [[i, bodega[1], bodega[0]] for i, bodega in enumerate(destino, start=1)]
                    print(tabulate(bodegas_destino, headers=['Nº', 'Nombre', 'Código'], tablefmt='fancy_grid'))

                    bodega_destino = input("Ingrese el número correspondiente a la bodega de origen(0 para cancelar): ")
                    if not bodega_destino.isdigit():
                        system('cls')
                        print("Por favor, ingrese un número.")
                        continue

                    bodega_destino = int(bodega_destino)

                    if producto_mover == 0:
                        input("\nPresione ENTER para volver atrás ...")
                        system('cls')
                        return                    
                    if bodega_destino < 1 or bodega_destino > len(destino):
                        system('cls')
                        print(f"Opción no válida, debe ser un número entre 1 y {len(destino)}.")
                    if cod_origen == destino[bodega_destino - 1][0]:
                        system('cls')
                        print("Error: La bodega de destino no puede ser la misma que la bodega de origen.")                   
                    else:
                        cod_destino = destino[bodega_destino - 1][0]
                        break  # Salir del bucle si la opción es válida
                


                usuario = user

                sql_last_id_mov = "select max(codmov) from movimientos"
                self.cursor.execute(sql_last_id_mov)
                last_cod_mov = self.cursor.fetchone()[0]

                if last_cod_mov is None:
                    next_number = 1
                    prefix = 'MOV'
                    codmovd = f"{prefix}{(next_number):02}"

                else:
                    prefix = last_cod_mov[:-2]
                    number = int(last_cod_mov[-2:])
                    next_number = number + 1
                    codmovd = f"{prefix}{(next_number):02}"
                
                codmovr = f"{prefix}{(next_number + 1):02}"

                fechamov = datetime.now()

                system('cls')

                tabla = []
                for cod_prod, stock in productos_a_mover:
                    tabla.append([cod_prod, stock, cod_origen, cod_destino])

                # Imprimir como tabla usando tabulate
                print("\nResumen de movimientos:")
                print(tabulate(tabla, headers=["Producto", "Stock a mover", "Desde Bodega", "Hacia Bodega"], tablefmt="fancy_grid"))

                # Confirmación para continuar
                confirmar = input("\n¿Desea proceder con los movimientos listados arriba? (s/n): ").strip().lower()

                while confirmar not in ['s', 'n']:
                    print("Respuesta no válida. Por favor ingrese 's' para confirmar o 'n' para cancelar.")
                    confirmar = input("\n¿Desea proceder con los movimientos listados arriba? (s/n): ").strip().lower()

                if confirmar == 'n':
                    print("Movimiento cancelado.")
                    input("\nPresione ENTER para volver atrás...")
                    system('cls')
                    return

                # Procesar el movimiento 
                for cod_prod, stock in productos_a_mover:
                    try:
                        # Obtener el último código de movimiento y generar el siguiente

                        # Insertar el movimiento de despacho
                        sql_movimiento_despacho = "insert into movimientos (codmov, codprod, tipomov, fechamov, stock, bodega, usuario) values (%s, %s, 'DESPACHO', %s, %s, %s, %s)"
                        self.cursor.execute(sql_movimiento_despacho, (codmovd, cod_prod, fechamov, stock, cod_origen, usuario))


                        # Insertar el movimiento de recepción
                        sql_movimiento_recepcion = "insert into movimientos (codmov, codprod, tipomov, fechamov, stock, bodega, usuario) values (%s, %s, 'RECEPCION', %s, %s, %s, %s)"
                        self.cursor.execute(sql_movimiento_recepcion, (codmovr, cod_prod, fechamov, stock, cod_destino, usuario))

                        # Actualizar el inventario de la bodega de origen
                        sql_inventario_despacho = "update inventario set stock = stock - %s where bodega = %s and codprod = %s"
                        self.cursor.execute(sql_inventario_despacho, (stock, cod_origen, cod_prod))

                        # Verificar si el producto está registrado en la bodega de destino
                        query_verificar_producto = "select * from inventario where codprod = %s and bodega = %s"
                        self.cursor.execute(query_verificar_producto, (cod_prod, cod_destino))
                        producto_existente = self.cursor.fetchone()

                        if producto_existente is None:
                            sql_last_id_inv = "select max(coding) from inventario"
                            self.cursor.execute(sql_last_id_inv)
                            last_cod_inv = self.cursor.fetchone()[0]
                            if last_cod_inv is None:
                                next_number = 1
                                prefix = 'ING'
                                codinv = f"{prefix}{next_number:02}"
                            else:
                                prefix = last_cod_inv[:-2]  
                                number = int(last_cod_inv[-2:])  
                                next_number = number + 1
                                codinv = f"{prefix}{next_number:02}"
                            
                            sql_agregar_producto = "insert into inventario (coding, codprod, bodega, stock) values (%s, %s, %s, 0)"
                            self.cursor.execute(sql_agregar_producto, (codinv, cod_prod, cod_destino))

                            # Actualizar el inventario de la bodega de destino
                        sql_inventario_recepcion = "update inventario set stock = stock + %s where bodega = %s and codprod = %s"
                        self.cursor.execute(sql_inventario_recepcion, (stock, cod_destino, cod_prod))

                        self.conexion.commit()
                        print("\nEl producto se movio con éxito.\n")
                        

                    except (ValueError, IndexError) as e:
                        print(f"Error: {e}")
                        self.conexion.rollback()
                        return
                input("\nPresione ENTER para volver atrás...")  

            except (ValueError, IndexError) as e:
                print(f"Error: {e}")
                self.conexion.rollback()
            except Exception as e:
                print(f"Error general: {e}")
                self.conexion.rollback()
            

        

mov=Movimientos()
