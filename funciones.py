import os
from conexion import conectar_db
from getpass import getpass
def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

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

# Función para gestionar bodegas
def gestionar_bodegas():
    try:
        print("\nGestionar Bodegas")
        print("1. Crear Bodega")
        print("2. Eliminar Bodega")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            crear_bodega()
        elif opcion == "2":
            eliminar_bodega()
        else:
            raise ValueError("Opción no válida.")
    except ValueError as e:
        print(f"{e}, regresando al menú anterior.")


# Función para crear una bodega
def crear_bodega():
    try:
        conexion = conectar_db()
        cursor = conexion.cursor()
        cod_bod = input("Ingrese el código de la bodega: ")
        sucursal = input("Ingrese la sucursal: ")
        fono_bod = input("Ingrese el teléfono de la bodega: ")
        responsable = input("Ingrese el responsable: ")
        cod_post_bod = input("Ingrese el código postal de la bodega: ")
        cursor.execute("INSERT INTO BODEGAS (CODBOD, SUCURSAL, FONOBOD, RESPONSABLE, CODPOSTBOD) VALUES (%s, %s, %s, %s, %s)",
                        (cod_bod, sucursal, fono_bod, responsable, cod_post_bod))
        conexion.commit()
        print("Bodega creada exitosamente.")
        input("Precione cualquier tecla para continuar...")
        cursor.close()
        conexion.close()
    except Exception as e:
        print(f"Error al crear bodega: {e}")

# Función para eliminar una bodega
def eliminar_bodega():
    conexion = conectar_db()
    cursor = conexion.cursor()

    cod_bod = input("Ingrese el código de la bodega a eliminar: ")
    cursor.execute("SELECT * FROM INVENTARIO WHERE CODBOD = %s", (cod_bod,))
    inventario = cursor.fetchone()

    if inventario:
        print("No se puede eliminar una bodega que contenga productos.")
    else:
        cursor.execute("DELETE FROM BODEGAS WHERE CODBOD = %s", (cod_bod,))
        conexion.commit()
        print("Bodega eliminada exitosamente.")

# Función para crear productos
def crear_producto():
    conexion = conectar_db()
    cursor = conexion.cursor()
    cod_prod = input("Ingrese el código del producto: ")
    tipo = input("Ingrese el tipo de producto (libro, revista, enciclopedia): ")
    descripcion = input("Ingrese la descripción del producto: ")
    print("Seleccione la editorial del producto:")
    cursor.execute("SELECT RUTEDIT, NOMBREDIT FROM EDITORIALES")
    editoriales = cursor.fetchall()
    for idx, editorial in enumerate(editoriales, start=1):
        print(f"{idx}. {editorial[1]}")
    print(f"{len(editoriales) + 1}. Otro")
    opcion_editorial = int(input("Seleccione una opción: "))
    if opcion_editorial == len(editoriales) + 1:
        editorial = input("Ingrese el nombre de la nueva editorial: ")
        rut_edit = input("Ingrese el RUT de la nueva editorial: ")
        fono_edit = input("Ingrese el teléfono de la nueva editorial: ")
        cod_post_edit = input("Ingrese el código postal de la nueva editorial: ")
        repres_legal = input("Ingrese el representante legal de la nueva editorial: ")
        cursor.execute("INSERT INTO EDITORIALES (RUTEDIT, NOMBREDIT, FONOEDIT, CODPOSTEDIT, REPRESLEGALDI) VALUES (%s, %s, %s, %s, %s)",
                        (rut_edit, editorial, fono_edit, cod_post_edit, repres_legal))
        editorial = rut_edit
    else:
        editorial = editoriales[opcion_editorial - 1][0]

    print("Seleccione el autor del producto:")
    cursor.execute("SELECT RUNAUTOR, NOMBRESAU, APPAUT, AMPAUT FROM AUTORES")
    autores = cursor.fetchall()
    for idx, autor in enumerate(autores, start=1):
        print(f"{idx}. {autor[1]} {autor[2]} {autor[3]}")
    print(f"{len(autores) + 1}. Otro")
    opcion_autor = int(input("Seleccione una opción: "))
    if opcion_autor == len(autores) + 1:
        nombres_au = input("Ingrese los nombres del nuevo autor: ")
        app_aut = input("Ingrese el apellido paterno del nuevo autor: ")
        amp_aut = input("Ingrese el apellido materno del nuevo autor: ")
        cod_post_au = input("Ingrese el código postal del nuevo autor: ")
        fono_au = input("Ingrese el teléfono del nuevo autor: ")
        run_autor = input("Ingrese el RUT del nuevo autor: ")
        cursor.execute("INSERT INTO AUTORES (RUNAUTOR, NOMBRESAU, APPAUT, AMPAUT, CODPOSTAU, FONOAU) VALUES (%s, %s, %s, %s, %s, %s)",
                        (run_autor, nombres_au, app_aut, amp_aut, cod_post_au, fono_au))
        autor = run_autor
    else:
        autor = autores[opcion_autor - 1][0]

    cursor.execute("INSERT INTO PRODUCTOS (CODPROD, TIPO, DESCRIPCION, EDITORIAL, JEFE_BOD) VALUES (%s, %s, %s, %s, %s)",
                    (cod_prod, tipo, descripcion, editorial, "jefe_bod")) # Ajustar jefe_bod según el usuario autenticado
    cursor.execute("INSERT INTO AUPROD (CODAUPROD, RUNAUTOR, CODPROD) VALUES (%s, %s, %s)",
                    (f"AP{cod_prod[-3:]}", autor, cod_prod))
    conexion.commit()
    print("Producto creado exitosamente.")

# Función para mover productos
def mover_productos():
    conexion = conectar_db()
    cursor = conexion.cursor()

    cod_prod = input("Ingrese el código del producto a mover: ")
    cant_mov = int(input("Ingrese la cantidad a mover: "))
    cod_bod_dest = input("Ingrese el código de la bodega de destino: ")
    usuario = input("Ingrese el nombre del usuario que realiza el movimiento: ")

    cursor.execute("SELECT STOCK FROM INVENTARIO WHERE CODPROD = %s", (cod_prod,))
    stock_actual = cursor.fetchone()[0]

    if stock_actual < cant_mov:
        print("No hay suficientes productos en la bodega de origen para realizar el movimiento.")
        return

    cursor.execute("UPDATE INVENTARIO SET STOCK = STOCK - %s WHERE CODPROD = %s", (cant_mov, cod_prod))
    cursor.execute("INSERT INTO MOVIMIENTOS (CODMOV, FECHAMOV, STOCK, CODPROD, BODEGA, USUARIO, TIPOMOV) VALUES (%s, NOW(), %s, %s, %s, %s, 'MOVIMIENTO')",
                    (f"MOV{cod_prod[-3:]}", cant_mov, cod_prod, cod_bod_dest, usuario))
    conexion.commit()
    print("Movimiento realizado exitosamente.")


# Función para gestionar autores
def gestionar_autores():
    print("\nGestionar Autores")
    print("1. Agregar Autor")
    print("2. Eliminar Autor")
    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        agregar_autor()
    elif opcion == "2":
        eliminar_autor()
    else:
        print("Opción no válida, regresando al menú anterior.")

# Función para agregar un autor
def agregar_autor():
    conexion = conectar_db()
    cursor = conexion.cursor()

    nombres_au = input("Ingrese los nombres del autor: ")
    app_aut = input("Ingrese el apellido paterno del autor: ")
    amp_aut = input("Ingrese el apellido materno del autor: ")
    cod_post_au = input("Ingrese el código postal del autor: ")
    fono_au = input("Ingrese el teléfono del autor: ")
    run_autor = input("Ingrese el RUT del autor: ")

    cursor.execute("INSERT INTO AUTORES (RUNAUTOR, NOMBRESAU, APPAUT, AMPAUT, CODPOSTAU, FONOAU) VALUES (%s, %s, %s, %s, %s, %s)",
                    (run_autor, nombres_au, app_aut, amp_aut, cod_post_au, fono_au))
    conexion.commit()
    print("Autor agregado exitosamente.")
# Función para eliminar un autor
def eliminar_autor():
    conexion = conectar_db()
    cursor = conexion.cursor()

    run_autor = input("Ingrese el RUT del autor a eliminar: ")
    cursor.execute("SELECT * FROM AUPROD WHERE RUNAUTOR = %s", (run_autor,))
    productos = cursor.fetchone()

    if productos:
        print("No se puede eliminar un autor que tenga productos asociados.")
    else:
        cursor.execute("DELETE FROM AUTORES WHERE RUNAUTOR = %s", (run_autor,))
        conexion.commit()
        print("Autor eliminado exitosamente.")

# Función para gestionar editoriales
def gestionar_editoriales():
    print("\nGestionar Editoriales")
    print("1. Agregar Editorial")
    print("2. Eliminar Editorial")
    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        agregar_editorial()
    elif opcion == "2":
        eliminar_editorial()
    else:
        print("Opción no válida, regresando al menú anterior.")

# Función para agregar una editorial
def agregar_editorial():
    conexion = conectar_db()
    cursor = conexion.cursor()

    nombredit = input("Ingrese el nombre de la editorial: ")
    rutedit = input("Ingrese el RUT de la editorial: ")
    fonoedit = input("Ingrese el teléfono de la editorial: ")
    codpostedit = input("Ingrese el código postal de la editorial: ")
    represlegaldi = input("Ingrese el representante legal de la editorial: ")

    cursor.execute("INSERT INTO EDITORIALES (RUTEDIT, NOMBREDIT, FONOEDIT, CODPOSTEDIT, REPRESLEGALDI) VALUES (%s, %s, %s, %s, %s)",
                    (rutedit, nombredit, fonoedit, codpostedit, represlegaldi))
    conexion.commit()
    print("Editorial agregada exitosamente.")

# Función para eliminar una editorial
def eliminar_editorial():
    conexion = conectar_db()
    cursor = conexion.cursor()

    rutedit = input("Ingrese el RUT de la editorial a eliminar: ")
    cursor.execute("SELECT * FROM PRODUCTOS WHERE EDITORIAL = %s", (rutedit,))
    productos = cursor.fetchone()

    if productos:
        print("No se puede eliminar una editorial que tenga productos asociados.")
    else:
        cursor.execute("DELETE FROM EDITORIALES WHERE RUTEDIT = %s", (rutedit,))
        conexion.commit()
        print("Editorial eliminada exitosamente.")

# Función para visualizar todas las bodegas
def visualizar_bodegas():
    conexion = conectar_db()
    cursor = conexion.cursor()

    cursor.execute("SELECT CODBOD, SUCURSAL FROM BODEGAS")
    bodegas = cursor.fetchall()

    print("\nListado de Bodegas:")
    for bodega in bodegas:
        print(f"Código: {bodega[0]}, Sucursal: {bodega[1]}")

# Función para generar informe de inventario
def generar_informe_inventario():
    conexion = conectar_db()
    cursor = conexion.cursor()

    visualizar_bodegas()

    bodega_seleccionada = input("Ingrese el código de la bodega para generar el informe: ")

    cursor.execute("SELECT COUNT(*) FROM INVENTARIO WHERE CODBOD = %s", (bodega_seleccionada,))
    total_productos = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM PRODUCTOS WHERE TIPO = 'Libro' AND JEFE_BOD = (SELECT RUNJEF FROM JEFEBODEGA WHERE CODBOD = %s)",
                    (bodega_seleccionada,))
    libros = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM PRODUCTOS WHERE TIPO = 'Cuaderno' AND JEFE_BOD = (SELECT RUNJEF FROM JEFEBODEGA WHERE CODBOD = %s)",
                    (bodega_seleccionada,))
    cuadernos = cursor.fetchone()[0]

    cursor.execute("SELECT NOMBREDIT FROM EDITORIALES WHERE RUTEDIT IN (SELECT EDITORIAL FROM PRODUCTOS WHERE JEFE_BOD = (SELECT RUNJEF FROM JEFEBODEGA WHERE CODBOD = %s))",
                    (bodega_seleccionada,))
    editoriales = cursor.fetchall()

    print(f"Informe de Inventario - Bodega {bodega_seleccionada}")
    print(f"Total de productos: {total_productos}")
    print(f"Libros: {libros}")
    print(f"Cuadernos: {cuadernos}")
    print("Editoriales:")
    for editorial in editoriales:
        print(f"- {editorial[0]}")

# Función para generar informe de historial de movimientos
def generar_informe_movimientos():
    conexion = conectar_db()
    cursor = conexion.cursor()

    visualizar_bodegas()

    bodega_seleccionada = input("Ingrese el código de la bodega para generar el informe: ")

    cursor.execute("SELECT CODMOV, FECHAMOV, BODEGA, USUARIO FROM MOVIMIENTOS WHERE BODEGA = %s", (bodega_seleccionada,))
    movimientos = cursor.fetchall()

    print(f"Informe de Movimientos - Bodega {bodega_seleccionada}")
    for movimiento in movimientos:
        print(f"ID del movimiento: {movimiento[0]}, Fecha: {movimiento[1]}, Bodega de destino: {movimiento[2]}, Usuario: {movimiento[3]}")


# Menú del jefe de bodega
def menu_jefe_bodega():
    while True:
        print("\n--- Menú Jefe de Bodega ---")
        print("1. Gestionar Bodegas")
        print("2. Crear Productos")
        print("3. Mover Productos")
        print("4. Gestionar Autores")
        print("5. Gestionar Editoriales")
        print("6. Visualizar todas las Bodegas")
        print("7. Generar Informe de Inventario")
        print("8. Generar Informe de Historial de Movimientos")
        print("9. Cerrar Sesión")
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            gestionar_bodegas()
        elif opcion == "2":
            crear_producto()
        elif opcion == "3":
            mover_productos()
        elif opcion == "4":
            gestionar_autores()
        elif opcion == "5":
            gestionar_editoriales()
        elif opcion == "6":
            visualizar_bodegas()
        elif opcion == "7":
            generar_informe_inventario()
        elif opcion == "8":
            generar_informe_movimientos()
        elif opcion == "9":
            print("Cerrando sesión...")
            cls()
            break
        else:
            print("Opción no válida. Por favor, seleccione una opción del menú.")

# Menú del bodeguero
def menu_bodeguero():
    while True:
        print("\n--- Menú Bodeguero ---")
        print("1. Mover Productos")
        print("2. Visualizar todas las Bodegas")
        print("3. Cerrar Sesión")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            mover_productos()
        elif opcion == "2":
            visualizar_bodegas()
        elif opcion == "3":
            print("Cerrando sesión...")
            break
        else:
            print("Opción no válida. Por favor, seleccione una opción del menú.")

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


"""
a
a
a
a
a
a
a
a
a
a
a
a
a
a
a
a
aaaaaaa
a
a
"""