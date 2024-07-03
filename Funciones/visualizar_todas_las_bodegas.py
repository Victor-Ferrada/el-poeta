import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Conexion_DB.conexion import conectar_db


# Función para visualizar todas las bodegas
def visualizar_bodegas():
    conexion = conectar_db()
    cursor = conexion.cursor()

    cursor.execute("SELECT CODBOD, SUCURSAL FROM BODEGAS")
    bodegas = cursor.fetchall()

    print("\nListado de Bodegas:")
    for bodega in bodegas:
        print(f"Código: {bodega[0]}, Sucursal: {bodega[1]}")