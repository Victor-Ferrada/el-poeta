import sys
import os
import time
from os import system
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import mysql.connector
import pwinput


class Usuarios():
    def __init__(self):
        self.conexion = mysql.connector.connect(
            host='localhost',
            user='root',
            password='inacap2023',
            database='elpoeta')
        self.cursor=self.conexion.cursor()
        self.usuario_actual=None

    def autenticar_usuario(self):
        try:
            while True:
                system('cls')
                print('-'*10+'Inicio de Sesión'+'-'*10+'\n')
                user = input('Ingrese su RUN: ')
                # Verificar si el usuario existe en JEFEBODEGA
                self.cursor.execute("SELECT * FROM JEFEBODEGA WHERE RUNJEF = %s", (user,))
                jefe = self.cursor.fetchone()
                self.cursor.execute("SELECT * FROM BODEGUEROS WHERE RUNBOD = %s", (user,))
                bodeguero = self.cursor.fetchone()
                if not jefe and not bodeguero:
                    system('cls')
                    print(f'Usuario {user} no encontrado en el sistema.')
                    input('\nPresione ENTER para volver atrás...')
                    continue

                if jefe:
                    print('\n'+'-'*5+'Bienvenido Jefe de Bodega '+user+'-'*5+'\n')
                    while True:
                        password = pwinput.pwinput('Ingrese su clave: ')
                        self.cursor.execute("SELECT PASSJEF FROM JEFEBODEGA WHERE RUNJEF = %s AND PASSJEF = %s", (user, password))
                        jefe_contraseña = self.cursor.fetchone()
                        if jefe_contraseña and password == jefe_contraseña[0]:
                            self.usuario_actual=user
                            system('cls')
                            for i in range(3, 0, -1):
                                system('cls')
                                print('Sesión iniciada como Jefe de Bodega.\n')
                                print(f"Redirigiendo en {i} segundos...", end='\r')
                                time.sleep(1)  
                            system('cls')
                            return 'jefe'
                        if password=='s':
                            print('Volviendo atrás...')
                            break
                        else:
                            system('cls')
                            print(f"\nClave incorrecta para el Jefe de Bodega {user}.\nIntente nuevamente (o ingrese 's' para volver atrás)\n")
                            
                if bodeguero:
                    print('\n'+'-'*5+'Bienvenido Bodeguero '+user+'-'*5+'\n')
                    while True:
                        password = pwinput.pwinput('Ingrese su clave: ')
                        self.cursor.execute("SELECT PASSBOD FROM BODEGUEROS WHERE RUNBOD = %s AND PASSBOD = %s", (user, password))
                        bodeguero_contraseña = self.cursor.fetchone()
                        if bodeguero_contraseña and password == bodeguero_contraseña[0]:
                            self.usuario_actual=user
                            system('cls')
                            for i in range(3, 0, -1):
                                system('cls')
                                print('Sesión iniciada como Bodeguero.\n')
                                print(f"Redirigiendo en {i} segundos...", end='\r')
                                time.sleep(1)  
                            system('cls')
                            return 'bodeguero'
                        if password=='s':
                            print('Volviendo atrás...')
                            break
                        else:
                            system('cls')
                            print(f"\nClave incorrecta para el Bodeguero {user}.\nIntente nuevamente (o ingrese 's' para volver atrás)\n")
        except Exception as e:
            print(f"Error al autenticar usuario: {e}")
            return None
        finally:
            self.cursor.close()
            self.conexion.close()
            
us=Usuarios()
us.autenticar_usuario()
