import mysql.connector
import pickle
import os
from os import system
import configparser

class ConexionBD:
    conexion = None

    @classmethod
    def conectar_db(cls):
        if cls.conexion is None:
            config = configparser.ConfigParser()
            config.read('config.ini')
            
            try:
                cls.conexion = mysql.connector.connect(
                    host=config['DATABASE']['host'],
                    user=config['DATABASE']['user'],
                    password=config['DATABASE']['password'],
                    database=config['DATABASE']['database']
                )
            except mysql.connector.Error as e:
                print(f"Error al conectar a la base de datos: {e}")
            except KeyError as e:
                print(f"Error en la configuración: {e}. Asegúrate de que el archivo config.ini está correctamente configurado.")
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

def guardar_terminos_y_condiciones(usuario):
    try:
        with open(f'{usuario}_terminos.pickle', 'wb') as f:
            pickle.dump(True, f)  # Guardar True para indicar términos aceptados
        return True
    except Exception as e:
        print(f"Error al guardar términos y condiciones para {usuario}: {e}")
        return False

def verificar_terminos_y_condiciones(usuario):
    try:
        with open(f'{usuario}_terminos.pickle', 'rb') as f:
            aceptado = pickle.load(f)
            return aceptado
    except FileNotFoundError:
        return False
    except Exception as e:
        print(f"Error al verificar términos y condiciones para {usuario}: {e}")
        return False