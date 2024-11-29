import tkinter as tk
from tkinter import messagebox

base_datos = {
    "alexander@gmail.com": {"contraseña": "123", "nombre": "Alexander Flores Facundo", "clave": 1, "tipo": "Alumno"},
    "isaac@gmail.com": {"contraseña": "456", "nombre": "Isaac Garcia Venegas", "clave": 2, "tipo": "Alumno"},
    "david@gmail.com": {"contraseña": "789", "nombre": "David Perez", "clave": 3, "tipo": "Profesor"}
}

class Usuario:
    def __init__(self, correo: str, contraseña: str):
        self.correo = correo
        self.contraseña = contraseña

    def inicio_sesion(self):
        correo = entry_correo.get()
        contraseña = entry_contraseña.get()

        if correo in base_datos and base_datos[correo]["contraseña"] == contraseña:
            usuario_autenticado = base_datos[correo]
            messagebox.showinfo("Bienvenido", f"¡Bienvenido, {usuario_autenticado['nombre']}!")
            if usuario_autenticado["tipo"] == "Alumno":
                alumno = Alumno(usuario_autenticado["nombre"], usuario_autenticado["clave"])
                alumno.mostrar_menu()
            elif usuario_autenticado["tipo"] == "Profesor":
                profesor = Profesor(usuario_autenticado["nombre"], usuario_autenticado["clave"])
                profesor.mostrar_menu()
        else:
            messagebox.showerror("Error", "Correo o contraseña incorrectos.")

class Alumno(Usuario):
    def __init__(self, nombre: str, clave: int):
        super().__init__(None, None)
        self.nombre = nombre
        self.clave = clave

    def mostrar_menu(self):
        ventana.quit()

        menu_ventana = tk.Tk()
        menu_ventana.title("Menú de Alumno")
        menu_ventana.geometry("500x300")

        boton_solicitar = tk.Button(menu_ventana, text="Solicitar consulta académica", font=("Arial", 14), command=self.solicitar_consulta_academica)
        boton_solicitar.pack(pady=10)

        boton_eliminar = tk.Button(menu_ventana, text="Eliminar consulta", font=("Arial", 14), command=self.eliminar_consulta)
        boton_eliminar.pack(pady=10)

        boton_actualizar = tk.Button(menu_ventana, text="Actualizar consulta", font=("Arial", 14), command=self.actualizar_consulta)
        boton_actualizar.pack(pady=10)

        menu_ventana.mainloop()

    def solicitar_consulta_academica(self):
        messagebox.showinfo("Solicitud", "Solicitando consulta académica...")

    def eliminar_consulta(self):
        messagebox.showinfo("Eliminar", "Eliminando consulta...")

    def actualizar_consulta(self):
        messagebox.showinfo("Actualizar", "Actualizando consulta...")

class Profesor(Usuario):
    def __init__(self, nombre: str, clave: int):
        super().__init__(None, None)
        self.nombre = nombre
        self.clave = clave

    def mostrar_menu(self):
        ventana.quit()

        menu_ventana = tk.Tk()
        menu_ventana.title("Menú de Profesor")
        menu_ventana.geometry("500x300")

        boton_gestionar = tk.Button(menu_ventana, text="Gestionar consultas", font=("Arial", 14), command=self.gestionar_consultas)
        boton_gestionar.pack(pady=10)

        boton_modificar = tk.Button(menu_ventana, text="Modificar duración de horario", font=("Arial", 14), command=self.modificar_duracion_horario)
        boton_modificar.pack(pady=10)

        boton_generar = tk.Button(menu_ventana, text="Generar horario", font=("Arial", 14), command=self.generar_horario)
        boton_generar.pack(pady=10)

        menu_ventana.mainloop()

    def gestionar_consultas(self):
        messagebox.showinfo("Gestionar", "Gestionando consultas...")

    def modificar_duracion_horario(self):
        messagebox.showinfo("Modificar", "Modificando duración de horario...")

    def generar_horario(self):
        messagebox.showinfo("Generar", "Generando horario...")

ventana = tk.Tk()
ventana.title("Sistema de Inicio de Sesión")

ventana.geometry("500x350")

ventana.config(bg="#f0f000")

label_correo = tk.Label(ventana, text="Correo:", font=("Arial", 14))
label_correo.grid(row=0, column=0, pady=10, padx=20, sticky="e")

entry_correo = tk.Entry(ventana, font=("Arial", 14))
entry_correo.grid(row=0, column=1, pady=10, padx=20)

label_contraseña = tk.Label(ventana, text="Contraseña:", font=("Arial", 14))
label_contraseña.grid(row=1, column=0, pady=10, padx=20, sticky="e")

entry_contraseña = tk.Entry(ventana, show="*", font=("Arial", 14))
entry_contraseña.grid(row=1, column=1, pady=10, padx=20)

usuario = Usuario(None, None)

boton_iniciar = tk.Button(ventana, text="Iniciar sesión", font=("Arial", 14), command=usuario.inicio_sesion, bg="#4CAF50", fg="white")
boton_iniciar.grid(row=2, column=0, columnspan=2, pady=20)

ventana.mainloop()

