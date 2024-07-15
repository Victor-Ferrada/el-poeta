import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import mysql.connector
from tabulate import tabulate

from gestionar_editoriales import Editoriales
from gestionar_autores import Autores


class Productos():
    def __init__(self):
         self.conexion = mysql.connector.connect(
             host='localhost',
             user='root',
             password='12345678',
             database='elpoeta')
         self.cursor = self.conexion.cursor()


    def seleccionar_editorial(self):
            
            editoriales = self.cargar_editoriales()   

            print("Seleccione la editorial del producto:")
            for i, editorial in enumerate(editoriales, start=1):
                print(f"{i}. {editorial[1]} \t(RUT: {editorial[0]})")          

            opcion_editorial = int(input("Ingrese el número correspondiente a la editorial: "))
            if opcion_editorial < 1 or opcion_editorial > len(editoriales):
                print("Opción no válida.")
                return        
            
    def agregar_producto(self):
        
            # Mostrar opciones de tipo de producto
            tipos_producto = {
                "Novela": "NOV",
                "Revista": "REV",
                "Poemario": "POE",
                "Ensayo": "ENS",
                "Otros": "OTR"
            }
            

            sql_autores = "SELECT runautor, nombresau, appatau FROM autores"

            Editoriales.mostrar_editoriales(self)

            nuevedit = input('Desea agregar una nueva editorial? s/n:')
            if nuevedit.lower() == 's':
                Editoriales.agregar_editorial(self)


            editoriales = Editoriales.cargar_editoriales(self)   

            print("Seleccione la editorial del producto:")
            for i, editorial in enumerate(editoriales, start=1):
                print(f"{i}. {editorial[1]} \t(RUT: {editorial[0]})")          

            opcion_editorial = int(input("Ingrese el número correspondiente a la editorial: "))
            if opcion_editorial < 1 or opcion_editorial > len(editoriales):
                print("Opción no válida.")

            rut_editorial = editoriales[opcion_editorial - 1][0]

            Autores.mostrar_autores(self)

            nuevaut = input('Desea agregar un nuevo autor? s/n:')
            if nuevaut.lower() == 's':
                Autores.agregar_autor(self)
            
            autores = Autores.cargar_autores(self)
            

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

            print("Seleccione el tipo de producto:")
            for i, tipo in enumerate(tipos_producto.keys(), start=1):
                print(f"{i}. {tipo}")

            opcion_tipo = int(input("Ingrese el número correspondiente al tipo de producto: "))
            if opcion_tipo < 1 or opcion_tipo > len(tipos_producto):
                print("Opción no válida.")
                return
            

            titulo = input("Ingrese el título del producto: ").upper()
            descripcion = input("Ingrese la descripción del producto: ").upper()
            jefeBod = input("Ingrese el RUN del jefe de bodega: ").strip().upper()

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
                    self.cursor.execute(sql_insertar_auprod, (last_cod_auprod, run_autor, codProd))

                    
                self.conexion.commit()
                print("\nProducto agregado exitosamente.\n")
            except ValueError:
                print("Ingrese un número válido para seleccionar la editorial, el autor o el tipo de producto.")
            except Exception as e:
                print(f"Error al agregar producto: {e}")
                self.conexion.rollback()



    def mostrar_productos(self):
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


    def menu(self):
        while True:
            print("----- MENÚ DE AUTORES -----")
            print("1. Agregar Producto")
            print("2. Mostrar Productos")
            print("3. Eliminar Producto")

            print("5. Salir")
            opcion = input("Ingrese una opción: ")

            if opcion == '1':
                self.agregar_producto()
            elif opcion == '2':
                self.mostrar_productos()
            elif opcion == '3':
                self.eliminar_producto()

            elif opcion == '5':
                print("Saliendo del programa...")
                break
            else:
                print("Opción no válida. Intente nuevamente.")



productos=Productos()


productos.menu()
