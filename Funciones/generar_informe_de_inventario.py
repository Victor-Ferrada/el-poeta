import sys
import os
from tabulate import tabulate
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Conexion_DB.conexion import conectar_db
from Funciones.visualizar_todas_las_bodegas import visualizar_bodegas
from Funciones.cls import cls

# Función para generar informe de inventario
def generar_informe_inventario():
    conexion = conectar_db()
    cursor = conexion.cursor()

    visualizar_bodegas()

    bodega_seleccionada = input("Ingrese el código de la bodega para generar el informe: ")
    cls()
    cursor.execute("SELECT SUM(stock) AS inventario_total FROM Movimientos WHERE bodega = %s", (bodega_seleccionada,))
    total_productos = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM Productos WHERE tipo = 'Libro' AND jefeBod = (SELECT responsable FROM Bodegas WHERE codBod = %s)",
                    (bodega_seleccionada,))
    libros = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM Productos WHERE tipo = 'Revista' AND jefeBod = (SELECT responsable FROM Bodegas WHERE codBod = %s)",
                    (bodega_seleccionada,))
    revistas = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM Productos WHERE tipo = 'Enciclopedia' AND jefeBod = (SELECT responsable FROM Bodegas WHERE codBod = %s)",
                    (bodega_seleccionada,))
    enciclopedias = cursor.fetchone()[0]

    cursor.execute("SELECT nomEdit FROM Editoriales WHERE rutEdit IN (SELECT editorial FROM Productos WHERE jefeBod = (SELECT responsable FROM Bodegas WHERE codBod = %s))",
                    (bodega_seleccionada,))
    editoriales = cursor.fetchall()

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
    input("\nPresione Enter para continuar...")
    cls()


generar_informe_inventario()













