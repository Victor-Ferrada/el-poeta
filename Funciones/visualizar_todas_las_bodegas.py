import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Funciones.otras_funciones import ConexionBD


# Función para visualizar todas las bodegas
class BodegaViewer:
    def __init__(self):
        self.conexion = ConexionBD.conectar_db()
        if self.conexion:
            self.cursor = self.conexion.cursor()

    def visualizar_bodegas(self):
        try:
            self.cursor.execute("SELECT CODBOD, SUCURSAL FROM BODEGAS")
            bodegas = self.cursor.fetchall()

            print("\nListado de Bodegas:")
            for bodega in bodegas:
                print(f"Código: {bodega[0]}, Sucursal: {bodega[1]}")
        except Exception as e:
            print(f"Error al visualizar las bodegas: {e}")
        finally:
            if self.conexion:
                self.cursor.close()
                self.conexion.close()