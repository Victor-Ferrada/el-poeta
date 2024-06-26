import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Conexion_DB.conexion import conectar_db
from Funciones.visualizar_todas_las_bodegas import visualizar_bodegas

# Función para generar informe de historial de movimientos
def generar_informe_movimientos():
    conexion = conectar_db()
    cursor = conexion.cursor()

    visualizar_bodegas()

    bodega_seleccionada = input("Ingrese el código de la bodega para generar el informe: ")

    cursor.execute("SELECT CODMOV, FECHAMOV, BODEGA, USUARIO FROM MOVIMIENTOS WHERE BODEGA = %s", (bodega_seleccionada,))
    movimientos = cursor.fetchall()

    print(f"Informe de Movimientos - Bodega {bodega_seleccionada}")
    for movimiento in movimientos:
        print(f"ID del movimiento: {movimiento[0]}, Fecha: {movimiento[1]}, Bodega de destino: {movimiento[2]}, Usuario: {movimiento[3]}")
