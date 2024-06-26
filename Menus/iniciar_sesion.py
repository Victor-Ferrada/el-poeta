from getpass import getpass
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Funciones.cls import cls
from bodeguero import menu_bodeguero
from jefe_de_bodega import menu_jefe_bodega
from Funciones.iniciar_sesion import autenticar_usuario


# Iniciar sesión
def iniciar_sesion():
    while True:
        print("\n--- Iniciar Sesión ---")
        usuario = input("Usuario: ")
        contrasena = getpass("Contraseña: ")

        perfil = autenticar_usuario(usuario, contrasena)

        if perfil == 'jefe':
            print("¡Bienvenido Jefe de Bodega!")
            input("Precione cualquier tecla para continuar...")
            cls()
            menu_jefe_bodega()
            break
        elif perfil == 'bodeguero':
            print("¡Bienvenido Bodeguero!")
            input("Precione cualquier tecla para continuar...")
            cls()
            menu_bodeguero()
            break
        else:
            print("Credenciales incorrectas. Intente nuevamente.")
# Ejecutar el inicio de sesión al ejecutar el archivo
if __name__ == "__main__":
    iniciar_sesion()