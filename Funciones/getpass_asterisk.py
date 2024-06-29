import msvcrt
import sys
import os

def ocultarpass(prompt='Introduce tu contraseña: '):
    print(prompt, end='', flush=True)
    password = ""
    while True:
        ch = msvcrt.getch()
        if ch in {b'\n', b'\r', b'\r\n'}:
            break
        elif ch == b'\b':
            if len(password) > 0:
                password = password[:-1]
                sys.stdout.write('\b \b')
        else:
            password += ch.decode()
            sys.stdout.write('*')
        sys.stdout.flush()
    print()
    return password