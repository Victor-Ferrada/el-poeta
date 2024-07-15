import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Funciones.cls import cls
from Funciones.terminos_condiciones import mostrar_terminos_y_condiciones
from Funciones.iniciar_sesion import Usuarios

def main():
    us=Usuarios()
    while True:
        cls()
        if mostrar_terminos_y_condiciones():
            perfil=us.autenticar_usuario()
            break
        else:
            print("Debe aceptar los términos y condiciones para continuar.")
        return perfil
if __name__ == "__main__":
    main()

main()