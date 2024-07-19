from os import system
import sys
import time
from Funciones.otras_funciones import guardar_terminos_y_condiciones,verificar_terminos_y_condiciones

def mostrar_terminos_y_condiciones(usuario):
    # Verificar si los términos ya han sido aceptados previamente
    if verificar_terminos_y_condiciones(usuario):
        print("Términos y condiciones de uso aceptados anteriormente.\n")
        return True
    while True:
        print("\nTérminos y Condiciones de Uso del Sistema de Gestión de Inventario de la Librería El gran Poeta")
        print("")
        print("1. Acceso y Uso del Sistema:")
        print("   - El acceso y uso de esta base de datos están reservados para el personal autorizado de la librería.")
        print("   - Los usuarios deben autenticarse utilizando credenciales válidas proporcionadas por la librería.")
        print("")
        print("2. Roles y Responsabilidades:")
        print("   - Los usuarios tendrán asignado un rol específico: jefe de bodega o bodeguero, dependiendo de sus responsabilidades dentro de la librería.")
        print("   - El jefe de bodega tiene autorización para crear y gestionar bodegas, así como para agregar y eliminar productos, autores y editoriales en la base de datos.")
        print("   - El bodeguero tiene permisos limitados para mover productos entre bodegas según las instrucciones del jefe de bodega.")
        print("")
        print("3. Gestión de Bodegas y Productos:")
        print("   - Solo el jefe de bodega puede crear nuevas bodegas y eliminar solo aquellas que no tengan productos y hayan sido creadas por él.")
        print("   - La creación y eliminación de productos también está restringida al jefe de bodega.")
        print("   - Se debe garantizar que todas las acciones de gestión de inventario estén documentadas adecuadamente.")
        print("")
        print("4. Movimiento de Productos:")
        print("   - El bodeguero puede solo hacer traslado de productos desde la bodega local asignada bajo la supervisión y autorización del jefe de bodega.")
        print("   - Se debe verificar la disponibilidad de productos antes de proceder con cualquier movimiento.")
        print("")
        print("5. Confidencialidad y Seguridad:")
        print("   - Los usuarios son responsables de mantener la confidencialidad de sus credenciales de inicio de sesión y de cualquier información sensible a la que accedan.")
        print("   - Se deben seguir las políticas de seguridad establecidas por la librería para proteger la integridad de los datos.")
        print("")
        print("6. Uso Aceptable:")
        print("   - El uso de la base de datos debe limitarse a actividades relacionadas con las funciones de la librería, como la gestión de inventarios y la información bibliográfica.")
        print("   - No se permite el acceso no autorizado o el uso indebido de la base de datos.")
        print("")
        print("7. Exención de Responsabilidad:")
        print("   - Los desarrolladores no se hacen responsables por el mal uso del programa o por las acciones de los usuarios que violen estos términos y condiciones.")
        print("")
        print("8. Modificaciones a los Términos y Condiciones:")
        print("   - La librería se reserva el derecho de modificar estos términos y condiciones en cualquier momento.")
        print("   - Los usuarios serán notificados de los cambios mediante notificación directa o publicación en el sitio web de la librería.")
        print("")
        aceptado = input("\n¿Acepta los términos y condiciones de uso? (s/n): ").lower()
        while aceptado not in ['s', 'n']:
            aceptado = input("\nOpción inválida. Ingrese una opción válida (s/n): ").lower()
        if aceptado == "s":
            if guardar_terminos_y_condiciones(usuario):
                system('cls')
                input('Términos y condiciones de uso aceptados. Presione ENTER para continuar...')
                system('cls')
                return True
            else:
                print(f"Error al guardar términos y condiciones para {usuario}.")
                return False
        elif aceptado == "n":
            system('cls')
            print("Debe aceptar los términos y condiciones de uso para utilizar el sistema.")
            opcion = input('\n¿Desea volver a los términos y condiciones de uso o salir del sistema?\n1. Volver\n2. Salir\n\n').lower()
            while opcion not in ['1', '2']:
                opcion = input("\nOpción inválida. Por favor, ingrese '1' para volver o '2' para salir: ").lower()
            if opcion == "1":
                system('cls')
                continue
            elif opcion == "2":
                system('cls')
                confirmar=input('¿Está seguro que desea cerrar el sistema? (s/n): ').lower()
                while confirmar not in ['s', 'n']:
                    confirmar = input("\nOpción inválida. Ingrese una opción válida (s/n): ").lower()
                if confirmar=='s':
                    for i in range(3, 0, -1):
                        system('cls')
                        print(f"Saliendo del sistema en {i} segundos...", end='\r')
                        time.sleep(1)
                    sys.exit()
                else:
                    system('cls')
                    continue
