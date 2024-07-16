import sys
import os
from tabulate import tabulate
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Funciones.otras_funciones import ConexionBD
from os import system
from Funciones.gestionar_bodegas import Bodegas
bd=Bodegas()



class InformeHistorial():
    def __init__(self):
        self.conexion = ConexionBD.conectar_db()
        if self.conexion:
            self.cursor = self.conexion.cursor()

    def generar_informe_movimientos(self):
        print('-'*10+'Informes de Movimientos de Bodegas'+'-'*10+'\n')
        bd.mostrar_bodegas()
        while True:
            bodega_seleccionada = input("Ingrese el código de la bodega para generar el informe (o 's' para salir): ").strip().upper()
            system('cls')
            if bodega_seleccionada=='S':
                    system('cls')
                    print("\nVolviendo al menú de Jefe de Bodega...\n")
                    return
            if bodega_seleccionada=='':
                    system('cls')
                    print('-'*10+'Informes de Movimientos de Bodegas'+'-'*10+'\n')
                    Bodegas().mostrar_bodegas()
                    print("Entrada vacía. Reintente.\n")
                    continue
            
            self.cursor.execute("SELECT * FROM bodegas WHERE codbod = %s", (bodega_seleccionada,))
            bodega_existe = self.cursor.fetchone()
            if not bodega_existe:
                system('cls')
                print('-'*10+'Informes de Movimientos de Bodegas'+'-'*10+'\n')
                bd.mostrar_bodegas()
                print(f"Bodega {bodega_seleccionada} no existe. Reintente.\n")
                continue
            # Consulta para movimientos de recepcion
            query_recepcion = """
            select 
                codmov as 'código de movimiento',
                codprod as 'código de producto',
                tipomov as 'tipo de movimiento',
                fechamov as 'fecha de movimiento',
                stock as 'stock',
                bodega as 'código de bodega',
                usuario as 'usuario'
            from 
                movimientos
            where 
                tipomov = 'RECEPCION'
                and bodega = %s
            """
            self.cursor.execute(query_recepcion, (bodega_seleccionada,))
            movimientos_recepcion = self.cursor.fetchall()
            
            # Consulta para movimientos de despacho
            query_despacho = """
            select 
                codmov as 'código de movimiento',
                codprod as 'código de producto',
                tipomov as 'tipo de movimiento',
                fechamov as 'fecha de movimiento',
                stock as 'stock',
                bodega as 'código de bodega',
                usuario as 'usuario'
            from 
                movimientos
            where 
                tipomov = 'DESPACHO'
                and bodega = %s
            """
            self.cursor.execute(query_despacho, (bodega_seleccionada,))
            movimientos_despacho = self.cursor.fetchall()

            # Mostrar tabla de movimientos de recepcion
            if movimientos_recepcion:
                headers_recepcion = ["Código de Movimiento", "Código de Producto", "Tipo de Movimiento", "Fecha de Movimiento", "Stock", "Código de Bodega", "Usuario"]
                print(f"\nInforme de Movimientos de recepcion - Bodega {bodega_seleccionada}\n")
                print(tabulate(movimientos_recepcion, headers_recepcion, tablefmt="fancy_grid"))
            else:
                print(f"\nNo se encontraron movimientos de recepcion para la bodega {bodega_seleccionada}.")

            # Mostrar tabla de movimientos de despacho
            if movimientos_despacho:
                headers_despacho = ["Código de Movimiento", "Código de Producto", "Tipo de Movimiento", "Fecha de Movimiento", "Stock", "Código de Bodega", "Usuario"]
                print(f"\nInforme de Movimientos de despacho - Bodega {bodega_seleccionada}\n")
                print(tabulate(movimientos_despacho, headers_despacho, tablefmt="fancy_grid"))
            else:
                print(f"\nNo se encontraron movimientos de despacho para la bodega {bodega_seleccionada}.\n")
            input("\nPresione ENTER para volver atrás...")
            print('-'*10+'Informes de Movimientos de Bodegas'+'-'*10+'\n')
            bd.mostrar_bodegas()
                
            

InformeHistorial().generar_informe_movimientos()

"""print('-'*10+'Informes de Movimientos de Bodegas'+'-'*10+'\n')
            bd.mostrar_bodegas()"""