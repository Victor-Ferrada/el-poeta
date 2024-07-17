import sys
import os
from os import system
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import mysql.connector
from tabulate import tabulate
from Funciones.gestionar_editoriales import Editoriales
from Funciones.gestionar_autores import Autores
from Funciones.otras_funciones import ConexionBD,validar_entero


class Productos():
    def __init__(self):
        self.conexion = ConexionBD.conectar_db()
        if self.conexion:
            self.cursor = self.conexion.cursor()

    def agregar_producto(self,usuario):
            # Mostrar opciones de tipo de producto
            tipos_producto = {
                "Novela": "NOV",
                "Revista": "REV",
                "Poemario": "POE",
                "Ensayo": "ENS",
                "Otros": "OTR"
            }
            system('cls')
            Editoriales.mostrar_editoriales(self)
            while True:
                nuevedit = input('¿Desea agregar una nueva editorial? (s/n): ').strip().lower()
                
                if nuevedit == 's':
                    system('cls')
                    Editoriales.agregar_editorial(self)  # Llama al método estático para agregar una nueva editorial
                    break
                elif nuevedit == 'n':
                    system('cls')
                    break  # Salir del bucle si el usuario responde 'n'
                else:
                    system('cls')
                    print("Respuesta no válida. Por favor ingrese 's' para agregar una editorial o 'n' para salir.")

            editoriales = Editoriales.cargar_editoriales(self) 
            while True:
                if not editoriales:
                    print('No existen ni se han agregado editoriales con las que trabajar')
                    input("\nPresione ENTER para volver al menú de productos...")
                    return

                print("Seleccione la editorial del producto:")
                tabla_editoriales = [[i, editorial[1], editorial[0]] for i, editorial in enumerate(editoriales, start=1)]
                print(tabulate(tabla_editoriales, headers=['Nº', 'Nombre', 'RUT'], tablefmt='fancy_grid'))

                opcion_editorial = input("Ingrese el número correspondiente a la editorial: ")
                if not opcion_editorial.isdigit():
                    system('cls')
                    print("Por favor, ingrese un número.")
                    continue

                opcion_editorial = int(opcion_editorial)
                if opcion_editorial < 1 or opcion_editorial > len(editoriales):
                    system('cls')
                    print("Opción no válida. Debe ser un número entre 1 y", len(editoriales))
                else:
                    rut_editorial = editoriales[opcion_editorial - 1][0]
                    break  # Salir del bucle si la opción es válida

            system('cls')
            Autores.mostrar_autores(self)
            while True:
                nuevaut = input('¿Desea agregar un nuevo autor? (s/n): ').strip().lower()
                if nuevaut == 's':
                    system('cls')
                    Autores.agregar_autor(self)  # Llama al método estático para agregar una nueva editorial
                elif nuevaut == 'n':
                    system('cls')
                    break  
                else:
                    system('cls')
                    print("Respuesta no válida. Por favor ingrese 's' para agregar un autor o 'n' para salir.")
            autores = Autores.cargar_autores(self)
            while not autores:
                print('No existen ni se han agregado autores con las que trabajar')
                input("\nPresione ENTER para volver al menú de productos...")
                return
            while True:
                autores_seleccionados = []
                agregar_otro_autor = 's'
                
                while agregar_otro_autor.lower() == 's':
                    system('cls')
                    print("Seleccione el autor del producto:")
                    tabla_autores=[[i, autor[1]+' '+autor[2],autor[0]] for i, autor in enumerate(autores, start=1)]
                    print(tabulate(tabla_autores, headers=['Nº', 'Nombre', 'RUN'], tablefmt='fancy_grid'))

                    opcion_autor = input("Ingrese el número correspondiente al autor: ").strip().lower()
                    

                    
                    if not opcion_autor.isdigit():
                        print("Por favor, ingrese un número.")
                        continue
                    
                    opcion_autor = int(opcion_autor)
                    
                    if opcion_autor < 1 or opcion_autor > len(autores):
                        system('cls')
                        print("Opción no válida. Debe ser un número entre 1 y", len(autores))
                        continue
                    
                    run_autor = autores[opcion_autor - 1][0]
                    autores_seleccionados.append(run_autor)
                    
                    agregar_otro_autor = input("¿Desea agregar otro autor? (s/n): ").strip().lower()
                    
                    while agregar_otro_autor not in ['s', 'n']:
                        system('cls')
                        print("Respuesta no válida. Por favor ingrese 's' para agregar otro autor o 'n' para terminar.")
                        agregar_otro_autor = input("¿Desea agregar otro autor? (s/n): ").strip().lower()
                
                if not autores_seleccionados:
                    print("Debe seleccionar al menos un autor.")
                    continue
                
                break

            system('cls')
            print("Seleccione el tipo de producto:")
            for i, tipo in enumerate(tipos_producto.keys(), start=1):
                print(f"{i}. {tipo}")
            opcion_tipo = int(input("Ingrese el número correspondiente al tipo de producto: "))
            if opcion_tipo < 1 or opcion_tipo > len(tipos_producto):
                print("Opción no válida.")
                return
            
            system('cls')
            titulo = input("Ingrese el título del producto: ").strip().upper()
            while titulo=='':
                titulo = input("El título del producto no puede estar vacío. Ingrese nuevamente: ").strip().upper()            
            descripcion = input("Ingrese la descripción del producto: ").upper()
            jefeBod = usuario
            tipo_producto = list(tipos_producto.keys())[opcion_tipo - 1]
            cont = 1
            while True:
                codProd = f"{tipos_producto[tipo_producto]}{str(cont).zfill(3)}"
                self.cursor.execute("select * from productos where codprod = %s", (codProd,))
                resultado = self.cursor.fetchone()
                if not resultado:
                    break
                cont += 1
            try:
            # Insertar producto en la tabla PRODUCTOS
                sql_insertar_producto = "insert into productos (codprod, nomprod, tipo, descripcion, editorial, jefebod) values (%s, %s, %s, %s, %s, %s)"
                self.cursor.execute(sql_insertar_producto, (codProd, titulo, tipo_producto, descripcion, rut_editorial, jefeBod))

                # Generar código de auprod (auprod)
                sql_last_id_auprod = "select max(codauprod) from auprod"
                self.cursor.execute(sql_last_id_auprod)
                last_cod_auprod = self.cursor.fetchone()[0]

                if last_cod_auprod is None:
                    next_number = 1
                    prefix = 'AP'
                    next_cod_auprod = f"{prefix}{next_number:02}" 
                else:
                    prefix = last_cod_auprod[:-2]  
                    number = int(last_cod_auprod[-2:])  
                    next_number = number + 1
                    next_cod_auprod = f"{prefix}{next_number:02}" 


                # Insertar relación auprod (autor-producto)
                for run_autor in autores_seleccionados:
                    sql_insertar_auprod = "insert into auprod (codauprod, runautor, codprod) values (%s, %s, %s)"
                    self.cursor.execute(sql_insertar_auprod, (next_cod_auprod, run_autor, codProd))
                    next_number += 1  
                    next_cod_auprod = f"{prefix}{next_number:02}"  
                self.conexion.commit()
                print("\nProducto agregado exitosamente.\n")
                input("\nPresione ENTER para volver al menú de productos...")                
            except ValueError:
                print("Ingrese un número válido para seleccionar la editorial, el autor o el tipo de producto.")
            except Exception as e:
                print(f"Error al agregar producto: {e}")
                self.conexion.rollback()


    def mostrar_productos(self):
        print('-'*10+'Productos'+'-'*10+'\n')
        sql=f"""SELECT p.codProd, p.nomProd, p.tipo, p.descripcion, e.nomEdit, GROUP_CONCAT(a.apPatAu SEPARATOR ', ') AS apellidosAutores
            FROM Productos p
            JOIN Editoriales e ON p.editorial = e.rutEdit
            JOIN AuProd ap ON p.codProd = ap.codProd
            JOIN Autores a ON ap.runAutor = a.runAutor
            GROUP BY p.codProd, p.nomProd, p.tipo, p.descripcion, e.nomEdit;
            """
        try:
            self.cursor.execute(sql)
            lista=self.cursor.fetchall()
            lista_procesada = [[(campo if campo else "S/I") for campo in fila] for fila in lista]  
            print(tabulate(lista_procesada,headers=['Código','Nombre','Tipo','Descripcion','Editorial','Autores'],tablefmt='fancy_grid')) 
            print("\n")
        except Exception as e:
            print(f"Error al mostrar editoriales: {e}")
            self.conexion.rollback()

    def eliminar_producto(self, usuario):
        print('-'*10 + 'Eliminar Productos' + '-'*10 + '\n')
        Productos().mostrar_productos()
        while True:
            try:
                codProd = input("Ingrese el código del producto a eliminar (o 's' para salir): ").upper()

                if codProd == 'S':
                    system('cls')
                    print("\nVolviendo al menú de editoriales...\n")
                    return
                
                if codProd == '':
                    system('cls')
                    print('-'*10 + 'Eliminar Productos' + '-'*10 + '\n')
                    Productos().mostrar_productos()
                    print("Entrada vacía. Reintente.\n")
                    continue
                
                self.cursor.execute("select * from productos where codprod = %s", (codProd,))
                productos = self.cursor.fetchone()
                
                if not productos:
                    system('cls')
                    print('-'*10 + 'Eliminar Productos' + '-'*10 + '\n')
                    Productos().mostrar_productos()
                    print(f"Producto {codProd} no existe. Reintente.\n")
                    continue
                
                self.cursor.execute("select runjef from jefebodega")
                jefes = [jefe[0] for jefe in self.cursor.fetchall()]
                
                if usuario not in jefes:
                    system('cls')
                    print(f'Usuario {usuario} no autorizado para eliminar producto {codProd}. Por favor contacte al Jefe de Bodega.\n')
                    input('Presione ENTER para volver atrás...')
                    system('cls')
                    return
                
                self.cursor.execute("select * from inventario where codprod = %s", (codProd,))
                inventario = self.cursor.fetchone()
                
                if inventario:
                    system('cls')
                    print(f"\nNo se puede eliminar el producto {codProd} porque está registrado en inventario.\n")
                    input('Presione ENTER para volver atrás...')
                    print('-'*10 + 'Eliminar Productos' + '-'*10 + '\n')
                    Productos().mostrar_productos()
                    
                    continue
                
                confirmar = input(f"¿Está seguro que desea eliminar el producto {codProd}? (s/n): ").lower()
                    
                while confirmar not in ['s', 'n']:
                    confirmar = input("\nOpción inválida. Ingrese una opción válida (s/n): ").lower()
                
                if confirmar == 's':
                    try:
                        self.cursor.execute("delete from auprod where codprod = %s", (codProd,))               
                        self.cursor.execute("delete from productos where codprod = %s", (codProd,))
                        self.conexion.commit()
                        
                        print("\n")
                        Productos().mostrar_productos()
                        input("\nProducto eliminado exitosamente. Presione ENTER para volver al menú de productos...\n")
                        system('cls')
                        return
                    
                    except Exception as e:
                        print(f"Error al eliminar producto: {e}")
                        self.conexion.rollback()
                
                else:
                    system('cls')
                    input("Operación cancelada. Presione ENTER para volver al menú de productos...")
                    system('cls')
                    return 
            
            except Exception as e:
                print(f"Error inesperado: {e}")
                self.conexion.rollback()


    def cargar_productos(self):
        try:
            sql_productos = "select codprod, nomprod from productos"
            self.cursor.execute(sql_productos)
            productos = self.cursor.fetchall()
            return productos
        except Exception as e:
            print(f"Error al cargar productos: {e}")
            return []    


class Inventario():

    def __init__(self):
        self.conexion = ConexionBD.conectar_db()
        if self.conexion:
            self.cursor = self.conexion.cursor()

    def añadir_productos(self, usuario):
        try:
            productos = Productos.cargar_productos(self)
            while not productos:
                print('No existen ni se han agregado productos con los que trabajar')
                input("\nPresione ENTER para volver al menú de productos...")
                return
            
            system('cls')
            print('-'*10+'Productos Disponibles'+'-'*10+'\n')
            productos_list = [[i, producto[1], producto[0]] for i, producto in enumerate(productos, start=1)]
            print(tabulate(productos_list, headers=['Nº', 'Nombre', 'Código'], tablefmt='fancy_grid'))

            while True:
                try:
                    opcion_producto = input("\nIngrese el número del producto a inventariar (o 's' para salir): ")
                    if opcion_producto.lower() == 's':
                        system('cls')
                        print("\nVolviendo al menú principal...\n")
                        return
                    
                    if opcion_producto == '':
                        system('cls')
                        print('-'*10+'Productos Disponibles'+'-'*10+'\n')
                        productos_list = [[i, producto[1], producto[0]] for i, producto in enumerate(productos, start=1)]
                        print(tabulate(productos_list, headers=['Nº', 'Nombre', 'Código'], tablefmt='fancy_grid'))
                        print("Entrada vacía. Reintente.")
                        continue
                    
                    opcion_producto = int(opcion_producto)
                    
                    if opcion_producto < 1 or opcion_producto > len(productos):
                        print('-'*10+'Productos Disponibles'+'-'*10+'\n')
                        productos_list = [[i, producto[1], producto[0]] for i, producto in enumerate(productos, start=1)]
                        print(tabulate(productos_list, headers=['Nº', 'Nombre', 'Código'], tablefmt='fancy_grid'))
                        print("Opción no válida. Ingrese un número dentro del rango de opciones.")
                    
                        continue  # Volver a pedir la opción
                    
                    break  # Salir del bucle si la opción es válida
                
                except ValueError:
                    system('cls')
                    print('-'*10+'Productos Disponibles'+'-'*10+'\n')
                    productos_list = [[i, producto[1], producto[0]] for i, producto in enumerate(productos, start=1)]
                    print(tabulate(productos_list, headers=['Nº', 'Nombre', 'Código'], tablefmt='fancy_grid'))
                    print("Opción no válida. Ingrese un número dentro del rango de opciones.")

            cod_prod = productos[opcion_producto - 1][0]

            filtro_bodegas = usuario
            self.cursor.execute("select * from bodegas where responsable = %s", (filtro_bodegas,))
            bodegas = self.cursor.fetchall()

            while not bodegas:
                print('No existen ni se han agregado bodegas con las que trabajar')
                input("\nPresione ENTER para volver al menú de productos...")
                return

            system('cls')
            print('-'*10+'Bodegas Disponibles'+'-'*10+'\n')
            bodegas_list = [[i, bodega[1], bodega[0]] for i, bodega in enumerate(bodegas, start=1)]
            print(tabulate(bodegas_list, headers=['Nº', 'Sucursal', 'Código'], tablefmt='fancy_grid'))

            while True:
                try:
                    opcion_bodega = input("\nIngrese el número correspondiente a la bodega (o 's' para salir): ")
                    if opcion_bodega.lower() == 's':
                        system('cls')
                        print("\nVolviendo al menú principal...\n")
                        return
                    
                    if opcion_bodega == '':
                        system('cls')
                        print('-'*10+'Productos Disponibles'+'-'*10+'\n')
                        productos_list = [[i, producto[1], producto[0]] for i, producto in enumerate(productos, start=1)]
                        print(tabulate(productos_list, headers=['Nº', 'Nombre', 'Código'], tablefmt='fancy_grid'))
                        print("Entrada vacía. Reintente.")
                        continue
                    
                    opcion_bodega = int(opcion_bodega)
                    
                    if opcion_bodega < 1 or opcion_bodega > len(bodegas):
                        print('-'*10+'Productos Disponibles'+'-'*10+'\n')
                        productos_list = [[i, producto[1], producto[0]] for i, producto in enumerate(productos, start=1)]
                        print(tabulate(productos_list, headers=['Nº', 'Nombre', 'Código'], tablefmt='fancy_grid'))
                        print("Opción no válida. Ingrese un número dentro del rango de opciones.")
                        continue  # Volver a pedir la opción
                    
                    break  # Salir del bucle si la opción es válida
                
                except ValueError:
                    system('cls')
                    print('-'*10+'Productos Disponibles'+'-'*10+'\n')
                    productos_list = [[i, producto[1], producto[0]] for i, producto in enumerate(productos, start=1)]
                    print(tabulate(productos_list, headers=['Nº', 'Nombre', 'Código'], tablefmt='fancy_grid'))
                    print("Opción no válida. Ingrese un número dentro del rango de opciones.")

            cod_bodega = bodegas[opcion_bodega - 1][0]
            system('cls')

            while True:
                try:
                    stock = validar_entero("Ingrese el stock del producto: ", "stock")

                    if stock is None:
                        system('cls')
                        print("Entrada vacía. Reintente.\n")
                        continue
                    
                    break  # Salir del bucle si el stock es válido
                
                except ValueError:
                    system('cls')
                    print("Ingrese un número válido para el stock del producto.")

            try:
                # Verificar si el producto ya está en el inventario de la bodega
                self.cursor.execute("select stock from inventario where codprod = %s and bodega = %s", (cod_prod, cod_bodega))
                resultado = self.cursor.fetchone()

                if resultado:
                    # El producto ya está en el inventario, actualizar el stock
                    nuevo_stock = resultado[0] + stock
                    self.cursor.execute("update inventario set stock = %s where codprod = %s and bodega = %s", (nuevo_stock, cod_prod, cod_bodega))
                else:
                    # El producto no está en el inventario, insertar una nueva entrada
                    sql_last_id_inv = "select max(coding) from inventario"
                    self.cursor.execute(sql_last_id_inv)
                    last_cod_inv = self.cursor.fetchone()[0]

                    if last_cod_inv is None:
                        next_number = 1
                        prefix = 'ING'
                        next_cod_inv = f"{prefix}{next_number:02}"
                    else:
                        prefix = last_cod_inv[:-2]
                        number = int(last_cod_inv[-2:])
                        next_number = number + 1
                        next_cod_inv = f"{prefix}{next_number:02}"

                    sql_insertar_producto = "insert into inventario (coding, codprod, bodega, stock) values (%s, %s, %s, %s)"
                    self.cursor.execute(sql_insertar_producto, (next_cod_inv, cod_prod, cod_bodega, stock))

                self.conexion.commit()
                system('cls')
                input("\nProducto agregado exitosamente. Presione ENTER para volver atrás...\n")
                return
            except Exception as e:
                print(f"Error al agregar producto: {e}")
                self.conexion.rollback()

        except Exception as e:
            print(f"Error al agregar producto: {e}")
            self.conexion.rollback()

        
productos=Productos()
inventario=Inventario()