import tkinter as tk
from tkinter import messagebox
from funciones import autenticar_usuario, menu_jefe_bodega, menu_bodeguero

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión de Bodegas")
        self.create_login_screen()

    def create_login_screen(self):
        self.clear_screen()

        self.lbl_usuario = tk.Label(self.root, text="Usuario")
        self.lbl_usuario.pack()

        self.ent_usuario = tk.Entry(self.root)
        self.ent_usuario.pack()

        self.lbl_contrasena = tk.Label(self.root, text="Contraseña")
        self.lbl_contrasena.pack()

        self.ent_contrasena = tk.Entry(self.root, show="*")
        self.ent_contrasena.pack()

        self.btn_login = tk.Button(self.root, text="Iniciar Sesión", command=self.iniciar_sesion)
        self.btn_login.pack()

    def iniciar_sesion(self):
        usuario = self.ent_usuario.get()
        contrasena = self.ent_contrasena.get()
        perfil = autenticar_usuario(usuario, contrasena)

        if perfil == 'jefe':
            messagebox.showinfo("Login exitoso", "¡Bienvenido Jefe de Bodega!")
            self.menu_jefe_bodega()
        elif perfil == 'bodeguero':
            messagebox.showinfo("Login exitoso", "¡Bienvenido Bodeguero!")
            self.menu_bodeguero()
        else:
            messagebox.showerror("Error", "Credenciales incorrectas. Intente nuevamente.")

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def menu_jefe_bodega(self):
        self.clear_screen()

        tk.Label(self.root, text="--- Menú Jefe de Bodega ---").pack()

        tk.Button(self.root, text="Gestionar Bodegas", command=self.gestionar_bodegas).pack()
        tk.Button(self.root, text="Crear Productos", command=self.crear_producto).pack()
        tk.Button(self.root, text="Mover Productos", command=self.mover_productos).pack()
        tk.Button(self.root, text="Gestionar Autores", command=self.gestionar_autores).pack()
        tk.Button(self.root, text="Gestionar Editoriales", command=self.gestionar_editoriales).pack()
        tk.Button(self.root, text="Visualizar todas las Bodegas", command=self.visualizar_bodegas).pack()
        tk.Button(self.root, text="Generar Informe de Inventario", command=self.generar_informe_inventario).pack()
        tk.Button(self.root, text="Generar Informe de Historial de Movimientos", command=self.generar_informe_movimientos).pack()
        tk.Button(self.root, text="Cerrar Sesión", command=self.create_login_screen).pack()

    def menu_bodeguero(self):
        self.clear_screen()

        tk.Label(self.root, text="--- Menú Bodeguero ---").pack()

        tk.Button(self.root, text="Mover Productos", command=self.mover_productos).pack()
        tk.Button(self.root, text="Visualizar todas las Bodegas", command=self.visualizar_bodegas).pack()
        tk.Button(self.root, text="Cerrar Sesión", command=self.create_login_screen).pack()

    # Aquí puedes definir las funciones que se llaman en el menú
    def gestionar_bodegas(self):
        pass

    def crear_producto(self):
        pass

    def mover_productos(self):
        pass

    def gestionar_autores(self):
        pass

    def gestionar_editoriales(self):
        pass

    def visualizar_bodegas(self):
        pass

    def generar_informe_inventario(self):
        pass

    def generar_informe_movimientos(self):
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()