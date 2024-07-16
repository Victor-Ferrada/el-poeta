import sys
import os
from tabulate import tabulate
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import mysql.connector
from Funciones.gestionar_bodegas import Bodegas
bd = Bodegas()
from os import system


class MostrarInventario():
    def __init__(self):
        self.conexion = mysql.connector.connect(
            host='localhost',
            user='root',
            password='12345',
            database='elpoeta'
        )
        self.cursor = self.conexion.cursor()
        self.bd = Bodegas()

    def mostrar_bodegas(self):
        self.bd.mostrar_bodegas()

    def generar_informe_inventario(self):
        while True:
            self.mostrar_bodegas()

            bodega_seleccionada = input("Ingrese el código de la bodega para generar el informe (o 's' para salir): ")
            if bodega_seleccionada.lower() == 's':
                system('cls')
                self.cursor.close()
                self.conexion.close()
                return  # Salir del programa si se ingresa 's'

            system('cls')

            # Ejecutar consulta para verificar si la bodega seleccionada existe
            self.cursor.execute("SELECT COUNT(*) FROM Bodegas WHERE codBod = %s", (bodega_seleccionada,))
            bodega_existente = self.cursor.fetchone()[0]

            if bodega_existente > 0:
                break  # Salir del bucle si la bodega existe
            else:
                print(f"La bodega con código {bodega_seleccionada} no existe.")
                input("Presione Enter para continuar...")
                system('cls')

        # Ejecutar las consultas y generar el informe solo si la bodega existe
        self.cursor.execute("SELECT SUM(stock) AS inventario_total FROM Movimientos WHERE bodega = %s", (bodega_seleccionada,))
        total_productos = self.cursor.fetchone()[0]

        self.cursor.execute("SELECT COUNT(*) FROM Productos WHERE tipo = 'Libro' AND jefeBod = (SELECT responsable FROM Bodegas WHERE codBod = %s)",
                            (bodega_seleccionada,))
        libros = self.cursor.fetchone()[0]

        self.cursor.execute("SELECT COUNT(*) FROM Productos WHERE tipo = 'Revista' AND jefeBod = (SELECT responsable FROM Bodegas WHERE codBod = %s)",
                            (bodega_seleccionada,))
        revistas = self.cursor.fetchone()[0]

        self.cursor.execute("SELECT COUNT(*) FROM Productos WHERE tipo = 'Enciclopedia' AND jefeBod = (SELECT responsable FROM Bodegas WHERE codBod = %s)",
                            (bodega_seleccionada,))
        enciclopedias = self.cursor.fetchone()[0]

        self.cursor.execute("SELECT nomEdit FROM Editoriales WHERE rutEdit IN (SELECT editorial FROM Productos WHERE jefeBod = (SELECT responsable FROM Bodegas WHERE codBod = %s))",
                            (bodega_seleccionada,))
        editoriales = self.cursor.fetchall()

        # Preparar datos para tabulate
        data = [
            ["Total de productos", total_productos],
            ["Libros", libros],
            ["Revistas", revistas],
            ["Enciclopedias", enciclopedias]
        ]

        # Formato fancy_grid para tabulate
        table = tabulate(data, headers=["Categoría", "Cantidad"], tablefmt="fancy_grid")

        # Mostrar tabla
        print(f"Informe de Inventario - Bodega {bodega_seleccionada}")
        print(table)
        print("\nEditoriales:")
        for editorial in editoriales:
            print(f"- {editorial[0]}")

        # Opción para más información detallada
        while True:
            opcion = input("\nIngrese 'm' para más información sobre los productos o 's' para salir: ")
            if opcion.lower() == 's':
                system('cls')
                self.cursor.close()
                self.conexion.close()
                break
            elif opcion.lower() == 'm':
                # Mostrar información detallada de los productos
                self.cursor.execute("""
                    SELECT p.nomProd, e.nomEdit, i.stock
                    FROM Productos p
                    JOIN Editoriales e ON p.editorial = e.rutEdit
                    JOIN Inventario i ON p.codProd = i.codProd
                    WHERE i.bodega = %s
                """, (bodega_seleccionada,))
                productos = self.cursor.fetchall()

                data_productos = [["Producto", "Editorial", "Stock"]]
                data_productos.extend(productos)
                table_productos = tabulate(data_productos, headers="firstrow", tablefmt="fancy_grid")

                print("\nDetalles de los productos:")
                print(table_productos)
                input("\nPresione Enter para continuar...")
                system('cls')
                return
            else:
                print("Opción no válida. Intente de nuevo.")

    def cerrarBD(self):
        self.cursor.close()
        self.conexion.close()