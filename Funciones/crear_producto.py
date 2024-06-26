import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Conexion_DB.conexion import conectar_db


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