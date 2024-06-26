import mysql.connector

def conectar_db():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345678",
            database="elpoeta"
        )
        print("Conexión establecida.")
        return conexion
    except mysql.connector.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None #ola asasdasd hola