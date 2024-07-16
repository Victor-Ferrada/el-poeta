import sys
import os
from tabulate import tabulate
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Conexion_DB.conexion import conectar_db
from Funciones.gestionar_bodegas import Bodegas
bd=Bodegas()
from Funciones.cls import cls

# Función para generar informe de inventario
def generar_informe_inventario():
    conexion = conectar_db()
    cursor = conexion.cursor()

    while True:
        bd.mostrar_bodegas()

        bodega_seleccionada = input("Ingrese el código de la bodega para generar el informe (o 's' para salir): ")
        if bodega_seleccionada.lower() == 's':
            print("Saliendo del programa...")
            return  # Salir del programa si se ingresa 's'

        cls()
        
        # Ejecutar consulta para verificar si la bodega seleccionada existe
        cursor.execute("SELECT COUNT(*) FROM Bodegas WHERE codBod = %s", (bodega_seleccionada,))
        bodega_existente = cursor.fetchone()[0]

        if bodega_existente > 0:
            break  # Salir del bucle si la bodega existe
        else:
            print(f"La bodega con código {bodega_seleccionada} no existe.")
            input("Presione Enter para continuar...")
            cls()

    # Ejecutar las consultas y generar el informe solo si la bodega existe
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