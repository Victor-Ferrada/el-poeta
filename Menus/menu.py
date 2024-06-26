from iniciar_sesion import iniciar_sesion

def mostrar_terminos_y_condiciones():
    # Impresión de los términos y condiciones
    print("\nTérminos y Condiciones de Uso de la Base de Datos de la Biblioteca")
    print("1. Acceso y Uso del Sistema:")
    print("   - El acceso y uso de esta base de datos están reservados para el personal autorizado de la biblioteca.")
    print("   - Los usuarios deben autenticarse utilizando credenciales válidas proporcionadas por la biblioteca.")
    print("2. Roles y Responsabilidades:")
    print("   - Los usuarios tendrán asignado un rol específico: jefe de bodega o bodeguero, dependiendo de sus responsabilidades dentro de la biblioteca.")
    print("   - El jefe de bodega tiene autorización para crear y gestionar bodegas, así como para agregar y eliminar productos, autores y editoriales en la base de datos.")
    print("   - El bodeguero tiene permisos limitados para mover productos entre bodegas locales según las instrucciones del jefe de bodega.")
    print("3. Gestión de Bodegas y Productos:")
    print("   - Solo el jefe de bodega puede crear nuevas bodegas y eliminar aquellas que estén vacías de productos.")
    print("   - La creación y eliminación de productos también está restringida al jefe de bodega.")
    print("   - Se debe garantizar que todas las acciones de gestión de inventario estén documentadas adecuadamente.")
    print("4. Movimiento de Productos:")
    print("   - El bodeguero puede mover productos entre bodegas locales bajo la supervisión y autorización del jefe de bodega.")
    print("   - Se debe verificar la disponibilidad de productos antes de proceder con cualquier movimiento.")
    print("5. Confidencialidad y Seguridad:")
    print("   - Los usuarios son responsables de mantener la confidencialidad de sus credenciales de inicio de sesión y de cualquier información sensible a la que accedan.")
    print("   - Se deben seguir las políticas de seguridad establecidas por la biblioteca para proteger la integridad de los datos.")
    print("6. Uso Aceptable:")
    print("   - El uso de la base de datos debe limitarse a actividades relacionadas con las funciones de la biblioteca, como la gestión de inventarios y la información bibliográfica.")
    print("   - No se permite el acceso no autorizado o el uso indebido de la base de datos.")
    print("7. Exención de Responsabilidad:")
    print("   - Los desarrolladores no se hacen responsables por el mal uso del programa o por las acciones de los usuarios que violen estos términos y condiciones.")
    print("8. Modificaciones a los Términos y Condiciones:")
    print("   - La biblioteca se reserva el derecho de modificar estos términos y condiciones en cualquier momento.")
    print("   - Los usuarios serán notificados de los cambios mediante notificación directa o publicación en el sitio web de la biblioteca.")
    aceptado = input("\n¿Acepta los términos y condiciones? (s/n): ").lower()
    if aceptado == "s":
        return True
    else:
        return False

def iniciar_sesion():
    # Función simulada para iniciar sesión
    print("\nInicio de Sesión")
    # Aquí iría tu lógica real de inicio de sesión, por ejemplo:
    usuario = input("Ingrese su usuario: ")
    contrasena = input("Ingrese su contraseña: ")
    # Lógica de autenticación
    # Simplemente simulamos una autenticación exitosa para este ejemplo
    print(f"Bienvenido, {usuario}!")

def main():
    while True:
        if mostrar_terminos_y_condiciones():
            iniciar_sesion()
            # Aquí se implementaría la lógica para el resto de la aplicación según el perfil del usuario
            # Por ejemplo, mostrar menús diferentes para jefe de bodega y bodeguero.
            break
        else:
            print("Debe aceptar los términos y condiciones para continuar.")

if __name__ == "__main__":
    main()
