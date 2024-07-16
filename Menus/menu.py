import sys
import os
from os import system
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Funciones.cls import cls
from Funciones.terminos_condiciones import mostrar_terminos_y_condiciones
from Funciones.iniciar_sesion import Usuarios
from Menus.bodeguero import menu_bodeguero
from Menus.jefe_de_bodega import menu_jefe_bodega

def main():
    us=Usuarios()
    locales=None
    while True:
        try:
            print('-'*10+'Bienvenido al Sistema de Gestión de Inventario El gran Poeta'+'-'*10+'\n')
            print("1. Iniciar Sesión")
            print("2. Salir")
            opcion = input("\nSeleccione una opción: ")
            if opcion == "1":
                system('cls')
                perfil = us.autenticar_usuario()
                if perfil:
                    aceptado=mostrar_terminos_y_condiciones()
                    if aceptado:
                        if perfil == 'jefe':
                            # Redirigir al menú del Jefe de Bodega
                            print("Redirigiendo al menú del Jefe de Bodega...")
                            locales=menu_jefe_bodega(us.usuario_actual)  # Pasar el usuario actual al menú del jefe de bodega
                            
                        elif perfil == 'bodeguero':
                            # Redirigir al menú del Bodeguero
                            if locales==None:
                                locales=''
                                input('No hay bodegas locales creadas. \nPresione ENTER para volver al menú anterior...')
                                system('cls')
                                return
                            else:
                                print("Redirigiendo al menú del Bodeguero...")
                                menu_bodeguero(us.usuario_actual,locales)  # Pasar el usuario actual al menú del bodeguero
                    else:
                        sys.exit()
            elif opcion == "2":
                system('cls')
                confirmar=input('¿Está seguro que desea cerrar el sistema? (s/n): ')
                while confirmar not in ['s', 'n']:
                    confirmar = input("\nOpción inválida. Ingrese una opción válida (s/n): ").lower()
                if confirmar=='s':
                    for i in range(3, 0, -1):
                        system('cls')
                        print(f"Saliendo del sistema en {i} segundos...", end='\r')
                        time.sleep(1)
                    us.cerrarBD()
                    sys.exit()
                else:
                    system('cls')
                    continue
            else:
                system('cls')
                raise ValueError("Opción inválida.")
        except ValueError as e:
            print(f"{e} Ingrese una opción de la lista:\n")
        except Exception as e:
            print(f"Error inesperado: {e}")
            return

if __name__ == "__main__":
    main()

main()

