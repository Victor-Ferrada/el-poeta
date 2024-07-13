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