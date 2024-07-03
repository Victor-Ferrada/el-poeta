import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import mysql.connector
from Conexion_DB.conexion import conectar_db



class Bodegas():
    def __init__(self):
         self.conexion = mysql.connector.connect(
             host='localhost',
             user='root',
             password='inacap2023',
             database='elpoeta')
         self.cursor = self.conexion.cursor()
    # Función para crear una bodega 
    def crear_bodega():
        try:
            conexion = conectar_db()
            cursor = conexion.cursor()
            cod_bod = input("Ingrese el código de la bodega: ")
            sucursal = input("Ingrese la sucursal: ")
            fono_bod = input("Ingrese el teléfono de la bodega: ")
            responsable = input("Ingrese el responsable: ")
            cod_post_bod = input("Ingrese el código postal de la bodega: ")
            cursor.execute("INSERT INTO BODEGAS (CODBOD, SUCURSAL, FONOBOD, RESPONSABLE, CODPOSTBOD) VALUES (%s, %s, %s, %s, %s)",
                            (cod_bod, sucursal, fono_bod, responsable, cod_post_bod))
            conexion.commit()
            print("Bodega creada exitosamente.")
            input("Precione cualquier tecla para continuar...")
            cursor.close()
            conexion.close()
        except Exception as e:
            print(f"Error al crear bodega: {e}")

    # Función para eliminar una bodega  
    def eliminar_bodega():
        conexion = conectar_db()
        cursor = conexion.cursor()

        cod_bod = input("Ingrese el código de la bodega a eliminar: ")
        cursor.execute("SELECT * FROM INVENTARIO WHERE CODBOD = %s", (cod_bod,))
        inventario = cursor.fetchone()

        if inventario:
            print("No se puede eliminar una bodega que contenga productos.")
        else:
            cursor.execute("DELETE FROM BODEGAS WHERE CODBOD = %s", (cod_bod,))
            conexion.commit()
            print("Bodega eliminada exitosamente.")
Bodegas.crear_bodega()