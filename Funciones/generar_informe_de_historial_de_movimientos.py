import sys
import os
from tabulate import tabulate
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import mysql.connector
from os import system
from Funciones.gestionar_bodegas import Bodegas
bd=Bodegas()



class InformeHistorial():
    def __init__(self):
        self.conexion = mysql.connector.connect(
            host='localhost',
            user='root',
            password='inacap2023',
            database='elpoeta'
        )
        self.cursor = self.conexion.cursor()
        self.bd = Bodegas()

    def generar_informe_movimientos(self):
        self.bd.mostrar_bodegas()

        bodega_seleccionada = input("Ingrese el código de la bodega para generar el informe: ")
        system('cls')

        # Consulta para movimientos de recepcion
        query_recepcion = """
        SELECT 
            codMov AS 'Código de Movimiento',
            codProd AS 'Código de Producto',
            tipoMov AS 'Tipo de Movimiento',
            fechaMov AS 'Fecha de Movimiento',
            stock AS 'Stock',
            bodega AS 'Código de Bodega',
            usuario AS 'Usuario'
        FROM 
            Movimientos
        WHERE 
            tipoMov = 'recepcion'
            AND bodega = %s
        """
        self.cursor.execute(query_recepcion, (bodega_seleccionada,))
        movimientos_recepcion = self.cursor.fetchall()
        # Consulta para movimientos de despacho
        query_despacho = """
        SELECT 
            codMov AS 'Código de Movimiento',
            codProd AS 'Código de Producto',
            tipoMov AS 'Tipo de Movimiento',
            fechaMov AS 'Fecha de Movimiento',
            stock AS 'Stock',
            bodega AS 'Código de Bodega',
            usuario AS 'Usuario'
        FROM 
            Movimientos
        WHERE 
            tipoMov = 'despacho'
            AND bodega = %s
        """
        self.cursor.execute(query_despacho, (bodega_seleccionada,))
        movimientos_despacho = self.cursor.fetchall()

        # Mostrar tabla de movimientos de recepcion
        if movimientos_recepcion:
            headers_recepcion = ["Código de Movimiento", "Código de Producto", "Tipo de Movimiento", "Fecha de Movimiento", "Stock", "Código de Bodega", "Usuario"]
            print(f"\nInforme de Movimientos de recepcion - Bodega {bodega_seleccionada}\n")
            print(tabulate(movimientos_recepcion, headers_recepcion, tablefmt="fancy_grid"))
        else:
            print(f"No se encontraron movimientos de recepcion para la bodega {bodega_seleccionada}.")

        # Mostrar tabla de movimientos de despacho
        if movimientos_despacho:
            headers_despacho = ["Código de Movimiento", "Código de Producto", "Tipo de Movimiento", "Fecha de Movimiento", "Stock", "Código de Bodega", "Usuario"]
            print(f"\nInforme de Movimientos de despacho - Bodega {bodega_seleccionada}\n")
            print(tabulate(movimientos_despacho, headers_despacho, tablefmt="fancy_grid"))
        else:
            print(f"No se encontraron movimientos de despacho para la bodega {bodega_seleccionada}.")
        input("\nPresione ENTER para volver al menú Jefe de bodegas...")
    def cerrarBD(self):
        self.cursor.close()
        self.conexion.close()

# Ejemplo de uso
if __name__ == "__main__":
    informe = InformeHistorial()
    informe.generar_informe_movimientos()
    informe.cerrarBD()