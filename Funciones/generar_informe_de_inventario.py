import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Conexion_DB.conexion import conectar_db
from Funciones.visualizar_todas_las_bodegas import visualizar_bodegas


# Función para generar el informe de inventario por bodega
def generar_informe_inventario():
        # Conexión a la base de datos usando la función conectar_db
        connection = conectar_db()
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)

            # Mostrar las bodegas disponibles
            visualizar_bodegas()

            # Input para seleccionar una bodega por su código
            cod_bodega = input("Ingrese el código de la bodega para generar el informe: ")

            # Consulta para obtener el informe de inventario de una bodega específica
            query = """
                SELECT 
                    p.tipo,
                    COUNT(p.codProd) AS cantidad_productos
                FROM productos p
                WHERE p.jefeBod = (SELECT responsable FROM bodegas WHERE codBod = %s)
                GROUP BY p.tipo
            """
            cursor.execute(query, (cod_bodega,))
            inventario_bodega = cursor.fetchall()

            if inventario_bodega:
                print(f"Informe de inventario para la bodega {cod_bodega}:")
                total_productos = sum([prod['cantidad_productos'] for prod in inventario_bodega])
                print(f"Cantidad total de productos: {total_productos}")
                for producto in inventario_bodega:
                    print(f"Cantidad de {producto['tipo']}: {producto['cantidad_productos']}")
            else:
                print(f"No se encontró información para la bodega {cod_bodega}")




"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Conexion_DB.conexion import conectar_db
from Funciones.visualizar_todas_las_bodegas import visualizar_bodegas

# Función para generar informe de inventario
def generar_informe_inventario():
    conexion = conectar_db()
    cursor = conexion.cursor()

    visualizar_bodegas()

    bodega_seleccionada = input("Ingrese el código de la bodega para generar el informe: ")

    # Consulta para contar productos en la bodega seleccionada
    cursor.execute("SELECT COUNT(*) FROM Movimientos WHERE bodega = %s", (bodega_seleccionada,))
    total_productos = cursor.fetchone()[0]

    # Consulta para contar libros en la bodega seleccionada
    cursor.execute("SELECT COUNT(*) FROM Productos WHERE tipo = 'Libro' AND jefeBod IN (SELECT runJef FROM JefeBodega WHERE runJef = (SELECT responsable FROM Bodegas WHERE codBod = %s))", (bodega_seleccionada,))
    libros = cursor.fetchone()[0]

    # Consulta para contar cuadernos en la bodega seleccionada
    cursor.execute("SELECT COUNT(*) FROM Productos WHERE tipo = 'Cuaderno' AND jefeBod IN (SELECT runJef FROM JefeBodega WHERE runJef = (SELECT responsable FROM Bodegas WHERE codBod = %s))", (bodega_seleccionada,))
    cuadernos = cursor.fetchone()[0]

    # Consulta para obtener editoriales asociadas a productos en la bodega seleccionada
    cursor.execute("SELECT nomEdit FROM Editoriales WHERE rutEdit IN (SELECT editorial FROM Productos WHERE jefeBod IN (SELECT runJef FROM JefeBodega WHERE runJef = (SELECT responsable FROM Bodegas WHERE codBod = %s)))", (bodega_seleccionada,))
    editoriales = cursor.fetchall()

    print(f"Informe de Inventario - Bodega {bodega_seleccionada}")
    print(f"Total de productos: {total_productos}")
    print(f"Libros: {libros}")
    print(f"Cuadernos: {cuadernos}")
    print("Editoriales:")
    for editorial in editoriales:
        print(f"- {editorial[0]}")
"""