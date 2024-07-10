import sys
import os
from tabulate import tabulate
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Conexion_DB.conexion import conectar_db
from Funciones.gestion_bodega import mostrar_bodegas

# Función para generar informe de historial de movimientos
def generar_informe_movimientos():
    conexion = conectar_db()
    cursor = conexion.cursor()

    mostrar_bodegas()

    bodega_seleccionada = input("Ingrese el código de la bodega para generar el informe: ")

    cursor.execute("SELECT CODMOV, FECHAMOV, BODEGA, USUARIO FROM MOVIMIENTOS WHERE BODEGA = %s", (bodega_seleccionada,))
    movimientos = cursor.fetchall()

    if movimientos:
        headers = ["ID del movimiento", "Fecha", "Bodega de destino", "Usuario"]
        print(f"\nInforme de Movimientos - Bodega {bodega_seleccionada}\n")
        print(tabulate(movimientos, headers, tablefmt="fancy_grid"))
    else:
        print(f"No se encontraron movimientos para la bodega {bodega_seleccionada}.")
    input("\nPresione Enter para continuar...")

