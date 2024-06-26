import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Conexion_DB.conexion import conectar_db


# Función para autenticar usuarios
def autenticar_usuario(usuario, contrasena):
    try:
        conexion = conectar_db()
        cursor = conexion.cursor()

        cursor.execute("SELECT * FROM JEFEBODEGA WHERE RUNJEF = %s AND PASSJEF = %s", (usuario, contrasena))
        jefe = cursor.fetchone()

        if jefe:
            return 'jefe'
        
        cursor.execute("SELECT * FROM BODEGUEROS WHERE RUNBOD = %s AND PASSBOD = %s", (usuario, contrasena))
        bodeguero = cursor.fetchone()

        if bodeguero:
            return 'bodeguero'
    
        cursor.close()
        conexion.close()
    except Exception as e:
        print(f"Error al autenticar usuario: {e}")
        return None