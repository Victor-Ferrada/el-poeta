import mysql.connector
import pickle
import os
from os import system
class ConexionBD:
    conexion = None

    @classmethod
    def conectar_db(cls):
        if cls.conexion is None:
            try:
                cls.conexion = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="inacap2023",
                    database="elpoeta"
                )
            except mysql.connector.Error as e:
                print(f"Error al conectar a la base de datos: {e}")
        return cls.conexion
    
    def cerrar_db(cls):
        if cls.conexion:
            cls.conexion.close()
            cls.conexion = None

def validar_entero(mensaje,campo):
    while True:
        try:
            valor = int(input(mensaje).strip())
            if valor > 0:
                return valor
            else:
                system('cls')
                print(f"\nEl {campo} debe ser positivo. Intente nuevamente.\n")
        except ValueError:
            print(f"\nEntrada inválida. El {campo} debe ser un número. Intente nuevamente.")
            pass

def save_locales(locales):
    """Guardar locales en el archivo locales.pickle."""
    with open(LOCALES_FILE, 'wb') as f:
        pickle.dump(locales, f)


def load_locales():
    """Cargar locales desde el archivo locales.pickle si existe."""
    if os.path.exists(LOCALES_FILE):
        with open(LOCALES_FILE, 'rb') as f:
            locales = pickle.load(f)
        return locales
    return None
LOCALES_FILE = "locales.pickle"