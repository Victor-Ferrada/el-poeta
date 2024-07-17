import sys
import os
from tabulate import tabulate
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Funciones.otras_funciones import ConexionBD
from Funciones.gestionar_bodegas import Bodegas
bd = Bodegas()
from os import system



def generar_informe_inventario():
    conexion = ConexionBD.conectar_db()
    if conexion:
        cursor = conexion.cursor()
    print('-'*10+'Informes de Inventario de Bodegas'+'-'*10+'\n')
    bd.mostrar_bodegas()
    while True:
        bodega_seleccionada = input("Ingrese el código de la bodega para generar el informe (o 's' para salir): ").upper()
        system('cls')
        if bodega_seleccionada == 'S':
            system('cls')
            print("\nVolviendo al menú de Jefe de Bodega...")
            return  # Salir del programa si se ingresa 's'
        elif bodega_seleccionada=='':
            system('cls')
            print('-'*10+'Informes de Inventario de Bodegas'+'-'*10+'\n')
            Bodegas().mostrar_bodegas()
            print("Entrada vacía. Reintente.\n")
            continue
        
        # Ejecutar consulta para verificar si la bodega seleccionada existe
        cursor.execute("select count(*) from bodegas where codbod = %s", (bodega_seleccionada,))
        bodega_existente = cursor.fetchone()[0]

        if not bodega_existente:
            system('cls')
            print('-'*10+'Informes de Movimientos de Bodegas'+'-'*10+'\n')
            bd.mostrar_bodegas()
            print(f"Bodega {bodega_seleccionada} no existe. Reintente.\n")
            continue

        # Ejecutar las consultas y generar el informe solo si la bodega existe
        cursor.execute("select sum(stock) as inventario_total from inventario where bodega = %s", (bodega_seleccionada,))
        total_productos = cursor.fetchone()[0]
        if total_productos==None:
            total_productos=0
        # Consulta para obtener el stock de libros en la bodega seleccionada
        cursor.execute("""
            select sum(stock) as stock_libros
            from inventario i
            join productos p on i.codprod = p.codprod
            where p.tipo = 'Libro' and i.bodega = %s
        """, (bodega_seleccionada,))
        stock_libros = cursor.fetchone()[0]
        if stock_libros==None:
            stock_libros=0
        # Consulta para obtener el stock de revistas en la bodega seleccionada
        cursor.execute("""
            select sum(stock) as stock_revistas
            from inventario i
            join productos p on i.codprod = p.codprod
            where p.tipo = 'Revista' and i.bodega = %s
        """, (bodega_seleccionada,))
        stock_revistas = cursor.fetchone()[0]
        if stock_revistas==None:
            stock_revistas=0
        # Consulta para obtener el stock de enciclopedias en la bodega seleccionada
        cursor.execute("""
            select sum(stock) as stock_enciclopedias
            from inventario i
            join productos p on i.codprod = p.codprod
            where p.tipo = 'Enciclopedia' and i.bodega = %s
        """, (bodega_seleccionada,))
        stock_enciclopedias = cursor.fetchone()[0]
        if stock_enciclopedias==None:
            stock_enciclopedias=0
        # Consulta para obtener el stock de poemarios en la bodega seleccionada
        cursor.execute("""
            select sum(stock) as stock_poemarios
            from inventario i
            join productos p on i.codprod = p.codprod
            where p.tipo = 'Poemario' and i.bodega = %s
        """, (bodega_seleccionada,))
        stock_poemarios = cursor.fetchone()[0]
        if stock_poemarios==None:
            stock_poemarios=0
        # Consulta para obtener el stock de otros en la bodega seleccionada
        cursor.execute("""
            select sum(stock) as stock_otros
            from inventario i
            join productos p on i.codprod = p.codprod
            where p.tipo = 'Otro' and i.bodega = %s
        """, (bodega_seleccionada,))
        stock_otros = cursor.fetchone()[0]
        if stock_otros==None:
            stock_otros=0

        # Preparar datos para tabulate
        data = [
            ["Total de productos", total_productos],
            ["Libros", stock_libros],
            ["Revistas", stock_revistas],
            ["Enciclopedias", stock_enciclopedias],
        ]

        
        table = tabulate(data, headers=["Categoría", "Cantidad"], tablefmt="fancy_grid")

        # Mostrar tabla
        system('cls')
        print(f"Informe de Inventario - Bodega {bodega_seleccionada}")
        print(table) 

        # Opción para más información detallada
        while True:
            opcion = input("\nIngrese 'm' para más información sobre los productos o 's' para salir: ").lower()
            while opcion not in ['s', 'm']:
                system('cls')
                print(f"Informe de Inventario - Bodega {bodega_seleccionada}")
                print(table) 
                opcion = input("\nOpción inválida.\n\nMás información (m)\nSalir (s)\n\nIngrese una opción válida: ").lower()
            if opcion == 's':
                system('cls')
                print('-'*10+'Informes de Inventario de Bodegas'+'-'*10+'\n')
                bd.mostrar_bodegas()
                break
            elif opcion == 'm':
                # Mostrar información detallada de los productos
                cursor.execute("""
                    select p.nomprod, e.nomedit, i.stock
                    from productos p
                    join editoriales e on p.editorial = e.rutedit
                    join inventario i on p.codprod = i.codprod
                    where i.bodega = %s
                    and p.tipo in ('Libro', 'Revista', 'Enciclopedia','Poemario','Otro')""", (bodega_seleccionada,))
                productos = cursor.fetchall()
                
                data_productos = [["Producto", "Editorial", "Stock"]]
                data_productos.extend(productos)
                table_productos = tabulate(data_productos, headers="firstrow", tablefmt="fancy_grid")

                print("\nDetalles de los productos:")
                print(table_productos)
                
                input("\nPresione ENTER para volver atrás...")
                system('cls')
                return
            else:
                print("Opción no válida. Intente de nuevo.")
