import sys
import os
import time
from os import system
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Funciones.terminos_condiciones import mostrar_terminos_y_condiciones
from Funciones.iniciar_sesion import Usuarios
from Menus.bodeguero import Bodegueros
from Menus.jefe_de_bodega import JefeBodega
from Funciones.otras_funciones import ConexionBD,load_locales,save_locales


def main():
    
    us=Usuarios()
    db=ConexionBD()
    jefe=JefeBodega()
    bod=Bodegueros()
    locales = load_locales()
    while True:
        try:
            print('-'*10+'Bienvenido al Sistema de Gestión de Inventario El gran Poeta'+'-'*10+'\n')
            print("1. Iniciar Sesión")
            print("2. Salir")
            opcion = input("\nSeleccione una opción: ")
            if opcion == "1":
                system('cls')
                perfil = us.autenticar_usuario()
                user=us.usuario_actual
                if perfil:
                    aceptado=mostrar_terminos_y_condiciones(user)
                    if aceptado:
                        if perfil == 'jefe':
                            # Redirigir al menú del Jefe de Bodega
                            print("Redirigiendo al menú del Jefe de Bodega...")
                            nuevo_locales = jefe.menu_jefe_bodega(user)  # Obtener locales actualizados desde el menú del jefe de bodega
                            if nuevo_locales:
                                locales = nuevo_locales  # Actualizar locales solo si se creó una bodega exitosamente
                            
                        elif perfil == 'bodeguero':
                            # Redirigir al menú del Bodeguero
                            print("Redirigiendo al menú del Bodeguero...")
                            bod.menu_bodeguero(user,locales)  # Pasar el usuario actual al menú del bodeguero
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
                    save_locales(locales) 
                    db.cerrar_db()
                    return locales
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

main()

