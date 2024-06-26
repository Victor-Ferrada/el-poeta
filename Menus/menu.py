# Importa las funciones necesarias para el inicio de sesión
from iniciar_sesion import iniciar_sesion

def mostrar_menu():
    print("\n--- Menú Principal ---")
    print("1. Iniciar Sesión")
    print("2. Salir")

def main():
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            iniciar_sesion()
        elif opcion == "2":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción no válida. Por favor, seleccione una opción del menú.")

if __name__ == "__main__":
    main()