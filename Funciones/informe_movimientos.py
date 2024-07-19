import sys
import os
from os import system
from tabulate import tabulate
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Funciones.otras_funciones import ConexionBD
from Funciones.gestionar_bodegas import Bodegas
bd=Bodegas()

def generar_informe_movimientos():
    conexion = ConexionBD.conectar_db()
    if conexion:
        cursor = conexion.cursor()
    print('-'*10+'Informes de Movimientos de Bodegas'+'-'*10+'\n')
    bd.mostrar_bodegas()
    while True:
        bodega_seleccionada = input("""- Ingrese 'g' para generar un informe de todas las bodegas.
                                    \n- Ingrese el código de la bodega para generar el informe individual.
                                    \n- Ingrese 's' para salir\tOpción: """).strip().upper()
        system('cls')
        try:            
            if bodega_seleccionada=='S':
                system('cls')
                print("\nVolviendo al menú de Jefe de Bodega...")
                return
            elif bodega_seleccionada=='':
                system('cls')
                print('-'*10+'Informes de Movimientos de Bodegas'+'-'*10+'\n')
                Bodegas().mostrar_bodegas()
                print("Entrada vacía. Reintente.\n")
                continue
            elif bodega_seleccionada=='G':
                query = """
                select 
                    d.codmov,
                    d.codprod,
                    concat(bo.sucursal, ' (', bo.codbod, ')') as sucursal_origen,
                    concat(bd.sucursal, ' (', bd.codbod, ')') as sucursal_destino,
                    d.fechamov,
                    d.usuario
                from 
                    movimientos d
                join 
                    movimientos r on d.fechamov = r.fechamov and d.codprod = r.codprod
                join
                    bodegas bo on d.bodega = bo.codbod
                join
                    bodegas bd on r.bodega = bd.codbod
                where 
                    d.tipoMov = 'DESPACHO' AND r.tipoMov = 'RECEPCION'
                order by 
                    d.fechaMov
                """
                cursor.execute(query)
                tmovimientos = cursor.fetchall()
                if tmovimientos:
                    system('cls')
                    headers = ["Código de Movimiento", "Código de Producto", "Sucursal de Origen", "Sucursal de Destino", "Fecha de Movimiento", "Usuario"]
                    print('-'*10+'Informe General de Movimientos'+'-'*10+'\n')
                    print(tabulate(tmovimientos, headers, tablefmt="fancy_grid"))
                else:
                    system('cls')
                    print("\nNo se encontraron movimientos en la base de datos.")
                input('Presione ENTER para volver atrás...')
                print('-'*10+'Informes de Movimientos de Bodegas'+'-'*10+'\n')
                bd.mostrar_bodegas()
                continue
            cursor.execute("select * from bodegas where codbod = %s", (bodega_seleccionada,))
            bodega_existe = cursor.fetchone()
            if not bodega_existe:
                system('cls')
                print('-'*10+'Informes de Movimientos de Bodegas'+'-'*10+'\n')
                bd.mostrar_bodegas()
                print(f"Bodega {bodega_seleccionada} no existe. Reintente.\n")
                continue
            query = """
            select 
                d.codmov,
                d.codprod,
                concat(bo.sucursal, ' (', bo.codbod, ')') as sucursal_origen,
                concat(bd.sucursal, ' (', bd.codbod, ')') as sucursal_destino,
                d.fechamov,
                d.usuario
            from 
                movimientos d
            join 
                movimientos r on d.fechamov = r.fechamov and d.codprod = r.codprod
            join
                bodegas bo on d.bodega = bo.codbod
            join
                bodegas bd on r.bodega = bd.codbod
            where 
                d.tipoMov = 'DESPACHO' and r.tipoMov = 'RECEPCION'
                and (d.bodega = %s or r.bodega = %s)
            order by 
                d.fechaMov
            """
            cursor.execute(query, (bodega_seleccionada, bodega_seleccionada))
            movimientos = cursor.fetchall()

            if movimientos:
                headers = ["Código de Movimiento", "Código de Producto", "Sucursal de Origen", "Sucursal de Destino", "Fecha de Movimiento", "Usuario"]
                print(f"\nInforme de Movimientos - Bodega {bodega_seleccionada}\n")
                print(tabulate(movimientos, headers, tablefmt="fancy_grid"))
            else:
                print(f"\nNo se encontraron movimientos para la bodega {bodega_seleccionada}.")

            input("\nPresione ENTER para volver atrás...")
            system('cls')
            print('-'*10+'Informes de Movimientos de Bodegas'+'-'*10+'\n')
            bd.mostrar_bodegas()
        except ValueError as e:
            print(f"{e} Ingrese una opción de la lista:\n")
        except Exception as e:
            print(f"Error inesperado: {e}")
            return
