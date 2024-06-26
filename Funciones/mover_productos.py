import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Conexion_DB.conexion import conectar_db


# Función para mover productos 
def mover_productos():
    conexion = conectar_db()
    cursor = conexion.cursor()

    cod_prod = input("Ingrese el código del producto a mover: ")
    cant_mov = int(input("Ingrese la cantidad a mover: "))
    cod_bod_dest = input("Ingrese el código de la bodega de destino: ")
    usuario = input("Ingrese el nombre del usuario que realiza el movimiento: ")

    cursor.execute("SELECT STOCK FROM INVENTARIO WHERE CODPROD = %s", (cod_prod,))
    stock_actual = cursor.fetchone()[0]

    if stock_actual < cant_mov:
        print("No hay suficientes productos en la bodega de origen para realizar el movimiento.")
        return

    cursor.execute("UPDATE INVENTARIO SET STOCK = STOCK - %s WHERE CODPROD = %s", (cant_mov, cod_prod))
    cursor.execute("INSERT INTO MOVIMIENTOS (CODMOV, FECHAMOV, STOCK, CODPROD, BODEGA, USUARIO, TIPOMOV) VALUES (%s, NOW(), %s, %s, %s, %s, 'MOVIMIENTO')",
                    (f"MOV{cod_prod[-3:]}", cant_mov, cod_prod, cod_bod_dest, usuario))
    conexion.commit()
    print("Movimiento realizado exitosamente.")