import sys
import os
from os import system
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import mysql.connector
from tabulate import tabulate
from Funciones.gestionar_editoriales import Editoriales
from Funciones.gestionar_autores import Autores
from Funciones.otras_funciones import ConexionBD


class Productos():
    def __init__(self):
        self.conexion = ConexionBD.conectar_db()
        if self.conexion:
            self.cursor = self.conexion.cursor()

    def agregar_producto(self,user):
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
                nuevedit = input('Desea agregar una nueva editorial? (s/n): ').strip().lower()
                
                if nuevedit == 's':
                    system('cls')
                    Editoriales.agregar_editorial(self)  # Llama al método estático para agregar una nueva editorial
                elif nuevedit == 'n':
                    system('cls')
                    break  # Salir del bucle si el usuario responde 'n'
                else:
                    system('cls')
                    print("Respuesta no válida. Por favor ingrese 's' para agregar una editorial o 'n' para salir.")

            editoriales = Editoriales.cargar_editoriales(self) 
            while not editoriales:
                print('No existen ni se han agregado editoriales con las que trabajar')
                input("\nPresione ENTER para volver al menú de productos...")                
                return
            print("Seleccione la editorial del producto:")
            for i, editorial in enumerate(editoriales, start=1):
                print(f"{i}. {editorial[1]} \t(RUT: {editorial[0]})")          
            opcion_editorial = int(input("Ingrese el número correspondiente a la editorial: "))
            if opcion_editorial < 1 or opcion_editorial > len(editoriales):
                print("Opción no válida.")
            rut_editorial = editoriales[opcion_editorial - 1][0]

            system('cls')
            Autores.mostrar_autores(self)
            while True:
                nuevaut = input('¿Desea agregar un nuevo autor? (s/n): ').strip().lower()
                if nuevaut == 's':
                    system('cls')
                    Autores.agregar_autor(self)  # Llama al método estático para agregar una nueva editorial
                elif nuevaut == 'n':
                    system('cls')
                    break  # Salir del bucle si el usuario responde 'n'
                else:
                    system('cls')
                    print("Respuesta no válida. Por favor ingrese 's' para agregar un autor o 'n' para salir.")
            autores = Autores.cargar_autores(self)
            while not autores:
                print('No existen ni se han agregado autores con las que trabajar')
                input("\nPresione ENTER para volver al menú de productos...")
                return
            autores_seleccionados = []
            agregar_otro_autor = 's'
            while agregar_otro_autor.lower() == 's':
                print("Seleccione el autor del producto:")
                for i, autor in enumerate(autores, start=1):
                    print(f"{i}. {autor[1]} (RUN: {autor[0]})")
                opcion_autor = int(input("Ingrese el número correspondiente al autor: "))
                if opcion_autor < 1 or opcion_autor > len(autores):
                    print("Opción no válida.")
                    continue
                run_autor = autores[opcion_autor - 1][0]
                autores_seleccionados.append(run_autor)
                agregar_otro_autor = input("¿Desea agregar otro autor? (s/n): ")

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
            jefeBod = user
            tipo_producto = list(tipos_producto.keys())[opcion_tipo - 1]
            cont = 1
            while True:
                codProd = f"{tipos_producto[tipo_producto]}{str(cont).zfill(3)}"
                self.cursor.execute("SELECT * FROM Productos WHERE codProd = %s", (codProd,))
                resultado = self.cursor.fetchone()
                if not resultado:
                    break
                cont += 1
            try:
            # Insertar producto en la tabla PRODUCTOS
                sql_insertar_producto = "INSERT INTO Productos (codProd, nomProd, tipo, descripcion, editorial, jefeBod) VALUES (%s, %s, %s, %s, %s, %s)"
                self.cursor.execute(sql_insertar_producto, (codProd, titulo, tipo_producto, descripcion, rut_editorial, jefeBod))

                # Generar código de auprod (auprod)
                sql_last_id_auprod = "SELECT MAX(codAuProd) FROM auprod"
                self.cursor.execute(sql_last_id_auprod)
                last_cod_auprod = self.cursor.fetchone()[0]

                if last_cod_auprod is None:
                    last_cod_auprod = 0
                last_cod_auprod = int(last_cod_auprod)
                codauprod = last_cod_auprod + 1

                # Insertar relación auprod (autor-producto)
                for run_autor in autores_seleccionados:
                    last_cod_auprod += 1
                    sql_insertar_auprod = "INSERT INTO auprod (codAuProd, runAutor, codProd) VALUES (%s, %s, %s)"
                    self.cursor.execute(sql_insertar_auprod, (codauprod, run_autor, codProd))
                self.conexion.commit()
                print("\nProducto agregado exitosamente.\n")
            except ValueError:
                print("Ingrese un número válido para seleccionar la editorial, el autor o el tipo de producto.")
            except Exception as e:
                print(f"Error al agregar producto: {e}")
                self.conexion.rollback()

    def mostrar_productos1(self):
        sql='select * from productos'
        try:
            self.cursor.execute(sql)
            lista=self.cursor.fetchall()  
            print(tabulate(lista,headers=['Nombre','Tipo','Descripcion','Rut Editorial','Rut Jefebodega'],tablefmt='github')) 
            print(tabulate(lista,headers=['Nombre','Tipo','Descripcion','Rut Editorial','Rut Jefebodega'],tablefmt='fancy_grid')) 
            print("\n")
        except Exception as e:
            print(f"Error al mostrar productos: {e}")
            self.conexion.rollback()

    def mostrar_productos(self):
        print('-'*10+'Productos'+'-'*10+'\n')
        sql='select * from productos'
        try:
            self.cursor.execute(sql)
            lista=self.cursor.fetchall()
            lista_procesada = [[(campo if campo else "S/I") for campo in fila] for fila in lista]  
            print(tabulate(lista_procesada,headers=['Nombre','Tipo','Descripcion','Rut Editorial','Rut Jefebodega'],tablefmt='fancy_grid')) 
            print("\n")
        except Exception as e:
            print(f"Error al mostrar editoriales: {e}")
            self.conexion.rollback()

    def eliminar_producto(self):
        Productos().mostrar_productos()
        codProd = input("Ingrese el codigo del producto a eliminar: ").upper()
        self.cursor.execute("SELECT * FROM INVENTARIO WHERE CODPROD = %s", (codProd,))
        inventario = self.cursor.fetchone()
        self.cursor.execute("SELECT * FROM PRODUCTOS WHERE CODPROD = %s", (codProd,))
        productos = self.cursor.fetchone()
        while not productos:
            codProd = input(f"El producto {codProd} no existe. Ingrese codigo nuevamente (o 's' para finalizar): ").upper()
            if codProd=='S':
                print("\nOperación cancelada.\n")
                return
            self.cursor.execute("SELECT * FROM PRODUCTOS WHERE RUNAUTOR = %s", (codProd,))
            productos = self.cursor.fetchone()
        if inventario:
            print("\nNo se puede eliminar un producto que se encuentra en bodega.\n")
        else:
            try:
                self.cursor.execute("DELETE FROM AUPROD WHERE CODPROD = %s", (codProd,))               
                self.cursor.execute("DELETE FROM PRODUCTOS WHERE CODPROD = %s", (codProd,))
                self.conexion.commit()
                print("\n")
                Productos().mostrar_productos()
                print("\nProducto eliminado exitosamente.\n")
            except Exception as e:
                print(f"Error al eliminar autor: {e}")
                self.conexion.rollback()

    def cargar_productos(self):
        try:
            sql_productos = "SELECT codprod, nomprod FROM productos"
            self.cursor.execute(sql_productos)
            productos = self.cursor.fetchall()
            return productos
        except Exception as e:
            print(f"Error al cargar productos: {e}")
            return []    

    def menu(self,user):
        while True:
            print("----- MENÚ DE PRODUCTOS -----")
            print("1. Agregar Producto")
            print("2. Mostrar Productos")
            print("3. Eliminar Producto")
            print("4. Añadir a Inventario")

            print("5. Salir")
            opcion = input("Ingrese una opción: ")

            if opcion == '1':
                self.agregar_producto(user)
            elif opcion == '2':
                self.mostrar_productos()
            elif opcion == '3':
                self.eliminar_producto(user)
            elif opcion == '4':
                Inventario.añadir_productos()

            elif opcion == '5':
                print("Saliendo del programa...")
                break
            else:
                print("Opción no válida. Intente nuevamente.")


class Inventario():

    def __init__(self):
        self.conexion = mysql.connector.connect(
            host='localhost',
            user='root',
            password='inacap2023',
            database='elpoeta')
        self.cursor = self.conexion.cursor()

    def añadir_productos(self,usuario):

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

        filtro_bodegas=usuario

        self.cursor.execute("SELECT * FROM BODEGAS WHERE RESPONSABLE= %s", (filtro_bodegas,))
       
       
        bodegas = self.cursor.fetchall()        


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


productos=Productos()
inventario=Inventario()

