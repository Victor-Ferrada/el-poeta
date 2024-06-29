from iniciar_sesion import iniciar_sesion
from Funciones.cls import cls
from Funciones.terminos_condiciones import mostrar_terminos_y_condiciones


def main():
    while True:
        cls()
        if mostrar_terminos_y_condiciones():
            iniciar_sesion()
            break
        else:
            print("Debe aceptar los términos y condiciones para continuar.")

if __name__ == "__main__":
    main()
