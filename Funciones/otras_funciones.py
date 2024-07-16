import mysql.connector

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
                print(f"\nEl {campo} debe ser positivo. Intente nuevamente.")
        except ValueError:
            print(f"\nEntrada inválida. El {campo} debe ser un número. Intente nuevamente.")
            pass
