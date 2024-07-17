import sys
import os
from tabulate import tabulate
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Funciones.otras_funciones import ConexionBD
from os import system
from Funciones.gestionar_bodegas import Bodegas
bd=Bodegas()

def generar_informe_movimientos():
    conexion = ConexionBD.conectar_db()
    if conexion:
        cursor = conexion.cursor()
    print('-'*10+'Informes de Movimientos de Bodegas'+'-'*10+'\n')
    bd.mostrar_bodegas()
    while True:
        bodega_seleccionada = input("Ingrese el código de la bodega para generar el informe (o 's' para salir): ").strip().upper()
        system('cls')
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
        
        cursor.execute("SELECT * FROM bodegas WHERE codbod = %s", (bodega_seleccionada,))
        bodega_existe = cursor.fetchone()
        if not bodega_existe:
            system('cls')
            print('-'*10+'Informes de Movimientos de Bodegas'+'-'*10+'\n')
            bd.mostrar_bodegas()
            print(f"Bodega {bodega_seleccionada} no existe. Reintente.\n")
            continue
        query = """
        SELECT 
            d.codMov,
            d.codProd,
            bo.sucursal AS sucursal_origen,
            bd.sucursal AS sucursal_destino,
            d.fechaMov,
            d.usuario
        FROM 
            Movimientos d
        JOIN 
            Movimientos r ON d.fechaMov = r.fechaMov AND d.codProd = r.codProd
        JOIN
            Bodegas bo ON d.bodega = bo.codBod
        JOIN
            Bodegas bd ON r.bodega = bd.codBod
        WHERE 
            d.tipoMov = 'DESPACHO' AND r.tipoMov = 'RECEPCION'
            AND (d.bodega = %s OR r.bodega = %s)
        ORDER BY 
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

