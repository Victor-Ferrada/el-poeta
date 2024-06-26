import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Conexion_DB.conexion import conectar_db


# Función para gestionar bodegas 
def gestionar_bodegas():
    try:
        print("\nGestionar Bodegas")
        print("1. Crear Bodega")
        print("2. Eliminar Bodega")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            crear_bodega()
        elif opcion == "2":
            eliminar_bodega()
        else:
            raise ValueError("Opción no válida.")
    except ValueError as e:
        print(f"{e}, regresando al menú anterior.")

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