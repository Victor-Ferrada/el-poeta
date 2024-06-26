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

    cursor.execute("SELECT COUNT(*) FROM INVENTARIO WHERE CODBOD = %s", (bodega_seleccionada,))
    total_productos = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM PRODUCTOS WHERE TIPO = 'Libro' AND JEFE_BOD = (SELECT RUNJEF FROM JEFEBODEGA WHERE CODBOD = %s)",
                    (bodega_seleccionada,))
    libros = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM PRODUCTOS WHERE TIPO = 'Cuaderno' AND JEFE_BOD = (SELECT RUNJEF FROM JEFEBODEGA WHERE CODBOD = %s)",
                    (bodega_seleccionada,))
    cuadernos = cursor.fetchone()[0]

    cursor.execute("SELECT NOMBREDIT FROM EDITORIALES WHERE RUTEDIT IN (SELECT EDITORIAL FROM PRODUCTOS WHERE JEFE_BOD = (SELECT RUNJEF FROM JEFEBODEGA WHERE CODBOD = %s))",
                    (bodega_seleccionada,))
    editoriales = cursor.fetchall()

    print(f"Informe de Inventario - Bodega {bodega_seleccionada}")
    print(f"Total de productos: {total_productos}")
    print(f"Libros: {libros}")
    print(f"Cuadernos: {cuadernos}")
    print("Editoriales:")
    for editorial in editoriales:
        print(f"- {editorial[0]}")