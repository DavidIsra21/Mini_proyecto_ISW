import tkinter as tk
from tkinter import messagebox

# ---------------------------- Clases ----------------------------

class Usuario:
    def __init__(self, nombre, correo, contraseña, clave):
        self.nombre = nombre
        self.correo = correo
        self.contraseña = contraseña
        self.clave = clave

class Estudiante(Usuario):
    def __init__(self, nombre, correo, contraseña, clave):
        super().__init__(nombre, correo, contraseña, clave)
        self.consultas = []

    def solicitar_consulta(self, consulta):
        self.consultas.append(consulta)

class Profesor(Usuario):
    def __init__(self, nombre, correo, contraseña, clave):
        super().__init__(nombre, correo, contraseña, clave)
        self.horarios = []
        self.consultas_gestionadas = []

    def registrar_horario(self, horario):
        self.horarios.append(horario)

    def gestionar_consulta(self, consulta, nuevo_estado):
        consulta.estado = nuevo_estado

class Horario:
    def __init__(self, fecha, hora_inicio, hora_final, duracion, id_horario, profesor):
        self.fecha = fecha
        self.hora_inicio = hora_inicio
        self.hora_final = hora_final
        self.duracion = duracion
        self.id_horario = id_horario
        self.profesor = profesor
        self.disponible = True

class Consulta:
    def __init__(self, fecha, hora_inicio, hora_final, profesor, alumno, id_consulta):
        self.fecha = fecha
        self.hora_inicio = hora_inicio
        self.hora_final = hora_final
        self.profesor = profesor
        self.alumno = alumno
        self.id_consulta = id_consulta
        self.estado = "solicitud"

# ---------------------- Base de Datos Simulada ----------------------

usuarios = {
    "profesor1@mail.com": Profesor("Prof. Juan", "profesor1@mail.com", "pass123", "P1"),
    "estudiante1@mail.com": Estudiante("Est. Ana", "estudiante1@mail.com", "pass456", "E1"),
    "profesor2": Profesor("Prof. Juan", "profesor1@mail.com", "123", "P1"),
    "estudiante2": Estudiante("Est. Ana", "estudiante1@mail.com", "456", "E1")
}

horarios = [
    Horario("2024-12-01", "10:00", "11:00", 60, "H1", "Prof. Juan")
]

consultas = []

# --------------------------- Sistema Principal ---------------------------

class SistemaConsultas:
    def __init__(self, root):
        self.root = root
        self.usuario_actual = None

        self.root.title("Sistema de Consultas Académicas")
        self.root.geometry("400x300")
        self.mostrar_pantalla_login()

    def mostrar_pantalla_login(self):
        self.limpiar_pantalla()
        '''
        tk.Label(self.root, text="Correo").pack()
        self.email_entry = tk.Entry(self.root)
        self.email_entry.pack()
        '''
        
        self.frame_login = tk.Frame(self.root)
        self.frame_login.pack(padx=10, pady=10)
        
        self.label_email = tk.Label(self.frame_login, text="Correo Electrónico:")
        self.label_email.grid(row=0, column=0, padx=5, pady=5)
        
        self.email_entry = tk.Entry(self.frame_login)
        self.email_entry.grid(row=0, column=1, padx=5, pady=5)

        '''
        tk.Label(self.root, text="Contraseña").pack()
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack()
        '''
        
        self.label_pass = tk.Label(self.frame_login, text="Contraseña:")
        self.label_pass.grid(row=1, column=0, padx=5, pady=5)

        self.password_entry = tk.Entry(self.frame_login, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Button(self.root, text="Iniciar Sesión", command=self.autenticar).pack()

    def autenticar(self):
        correo = self.email_entry.get()
        contraseña = self.password_entry.get()

        usuario = usuarios.get(correo)
        if usuario and usuario.contraseña == contraseña:
            self.usuario_actual = usuario
            if isinstance(usuario, Profesor):
                self.mostrar_menu_profesor()
            else:
                self.mostrar_menu_estudiante()
        else:
            messagebox.showerror("Error", "Correo o contraseña incorrectos")

    def mostrar_menu_profesor(self):
        self.limpiar_pantalla()

        label = tk.Label(self.root, text=f"Bienvenido, {self.usuario_actual.nombre}", font=("Arial", 16))
        label.pack(pady=10)
        #tk.Label(self.root, text=f"Bienvenido, {self.usuario_actual.nombre}").pack()
        tk.Button(self.root, text="Ver Notificaciones", command=self.ver_notificaciones_profesor).pack(pady= 5)
        tk.Button(self.root, text="Ver Consultas", command=self.gestionar_consultas).pack(pady= 5)
        tk.Button(self.root, text="Registrar Horario", command=self.registrar_horario).pack(pady= 5)
        tk.Button(self.root, text="Ver horarios disponibles", command=self.ver_horarios).pack(pady= 5)
        tk.Button(self.root, text="Modificar horario", command=self.modificar_horario).pack(pady= 5)
        tk.Button(self.root, text="Cerrar Sesión", command=self.mostrar_pantalla_login).pack(pady= 5)

    def mostrar_menu_estudiante(self):
        self.limpiar_pantalla()
        
        label = tk.Label(self.root, text=f"Bienvenido, {self.usuario_actual.nombre}", font=("Arial", 16))
        label.pack(pady=10)
        #tk.Label(self.root, text=f"Bienvenido, {self.usuario_actual.nombre}").pack()
        tk.Button(self.root, text="Solicitar Consulta", command=self.solicitar_consulta).pack(pady= 5)
        tk.Button(self.root, text="Ver Notificaciones", command=self.ver_notificaciones).pack(pady= 5)
        tk.Button(self.root, text="Ver horarios disponibles", command=self.mostrar_horarios).pack(pady= 5)
        tk.Button(self.root, text="Modificar o Cancelar consulta", command=self.modificar_consulta).pack(pady= 5)
        tk.Button(self.root, text="Cerrar Sesión", command=self.mostrar_pantalla_login).pack(pady= 5)

    def registrar_horario(self):
        self.limpiar_pantalla()
        tk.Label(self.root, text="Fecha (YYYY-MM-DD)").pack()
        self.fecha_entry = tk.Entry(self.root)
        self.fecha_entry.pack()

        tk.Label(self.root, text="Hora Inicio (HH:MM)").pack()
        self.hora_inicio_entry = tk.Entry(self.root)
        self.hora_inicio_entry.pack()

        tk.Label(self.root, text="Hora Final (HH:MM)").pack()
        self.hora_final_entry = tk.Entry(self.root)
        self.hora_final_entry.pack()

        tk.Button(self.root, text="Registrar", command=self.guardar_horario).pack()
        tk.Button(self.root, text="Volver", command=self.mostrar_menu_profesor).pack()

    def guardar_horario(self):
        fecha = self.fecha_entry.get()
        hora_inicio = self.hora_inicio_entry.get()
        hora_final = self.hora_final_entry.get()
        profesor = self.usuario_actual.nombre
        id_horario = f"H{len(horarios)+1}"

        nuevo_horario = Horario(fecha, hora_inicio, hora_final, 60, id_horario, profesor)
        horarios.append(nuevo_horario)
        self.usuario_actual.registrar_horario(nuevo_horario)
        messagebox.showinfo("Éxito", "Horario registrado correctamente")
        self.mostrar_menu_profesor()

    def solicitar_consulta(self):
        self.limpiar_pantalla()
        tk.Label(self.root, text="Seleccione un horario disponible:").pack()
        for horario in horarios:
            if horario.disponible:
                tk.Label(self.root, text=f"{horario.id_horario}: {horario.fecha} de {horario.hora_inicio} a {horario.hora_final}").pack()

        self.id_horario_entry = tk.Entry(self.root)
        self.id_horario_entry.pack()
        tk.Button(self.root, text="Solicitar", command=self.crear_consulta).pack()
        tk.Button(self.root, text="Volver", command=self.mostrar_menu_estudiante).pack()

    def crear_consulta(self):
        id_horario = self.id_horario_entry.get()
        horario = next((h for h in horarios if h.id_horario == id_horario and h.disponible), None)

        if horario:
            id_consulta = f"C{len(consultas)+1}"
            nueva_consulta = Consulta(horario.fecha, horario.hora_inicio, horario.hora_final, horario.profesor, self.usuario_actual.nombre, id_consulta)
            consultas.append(nueva_consulta)
            horario.disponible = False
            self.usuario_actual.solicitar_consulta(nueva_consulta)
            messagebox.showinfo("Éxito", "Consulta solicitada correctamente")
        else:
            messagebox.showerror("Error", "Horario no disponible")

        self.mostrar_menu_estudiante()

    def ver_notificaciones(self):
        self.limpiar_pantalla()
        tk.Label(self.root, text="Notificaciones:").pack()
        for consulta in self.usuario_actual.consultas:
            tk.Label(self.root, text=f"Consulta {consulta.id_consulta}: {consulta.estado}").pack()
        tk.Button(self.root, text="Volver", command=self.mostrar_menu_estudiante).pack()

    def gestionar_consultas(self):
        self.limpiar_pantalla()
        tk.Label(self.root, text="Gestión de Consultas:").pack()
        for consulta in consultas:
            if consulta.profesor == self.usuario_actual.nombre:
                tk.Label(self.root, text=f"Consulta {consulta.id_consulta} - Estado: {consulta.estado}").pack()

        self.id_consulta_entry = tk.Entry(self.root)
        self.id_consulta_entry.pack()
        tk.Button(self.root, text="Actualizar Estado", command=self.actualizar_estado).pack()
        tk.Button(self.root, text="Volver", command=self.mostrar_menu_profesor).pack()
    '''
    def actualizar_estado(self):
        id_consulta = self.id_consulta_entry.get()
        consulta = next((c for c in consultas if c.id_consulta == id_consulta), None)

        if consulta:
            self.limpiar_pantalla()
            tk.Label(self.root, text=f"Consulta {consulta.id_consulta} - Estado actual: {consulta.estado}").pack()

            estado_var = tk.StringVar(value="solicitud")
            opciones = ["aprobar", "rechazar"]

            if consulta.estado == "aprobada":
                opciones.append("cancelar")

            tk.Label(self.root, text="Seleccione el nuevo estado:").pack()
            for opcion in opciones:
                tk.Radiobutton(self.root, text=opcion.capitalize(), variable=estado_var, value=opcion).pack()

            tk.Button(self.root, text="Actualizar", command=lambda: self.guardar_nuevo_estado(consulta, estado_var.get())).pack()
            tk.Button(self.root, text="Volver", command=self.mostrar_menu_profesor).pack()
        else:
            messagebox.showerror("Error", "Consulta no encontrada")
            self.mostrar_menu_profesor()
        '''    
    def actualizar_estado(self):
        id_consulta = self.id_consulta_entry.get()
        consulta = next((c for c in consultas if c.id_consulta == id_consulta), None)

        if consulta:
            self.limpiar_pantalla()
            tk.Label(self.root, text=f"Consulta {consulta.id_consulta} - Estado actual: {consulta.estado}").pack()

            if consulta.estado != "cancelar" and consulta.estado != "rechazar":
                estado_var = tk.StringVar(value=consulta.estado)
                opciones = ["aprobar", "rechazar"]

                # Agregar opción de cancelar si la consulta ya está aprobada
                if consulta.estado == "aprobada":
                    opciones.append("cancelar")
                    opciones.remove("rechazar")

                tk.Label(self.root, text="Seleccione el nuevo estado:").pack()
                for opcion in opciones:
                    tk.Radiobutton(self.root, text=opcion.capitalize(), variable=estado_var, value=opcion).pack()

                tk.Button(self.root, text="Actualizar", command=lambda: self.guardar_nuevo_estado(consulta, estado_var.get())).pack()
                tk.Button(self.root, text="Volver", command=self.mostrar_menu_profesor).pack()
            else:
                messagebox.showerror("Error", "La consulta ya ha sido cancelada")
                self.mostrar_menu_profesor()
        else:
            messagebox.showerror("Error", "Consulta no encontrada")
            self.mostrar_menu_profesor()

    def guardar_nuevo_estado(self, consulta, nuevo_estado):
        if nuevo_estado == "aprobar":
            # Abrir interfaz para confirmación de cancelación
            self.interfaz_cancelar_consulta(consulta)
        else:
            consulta.estado = nuevo_estado
            messagebox.showinfo("Éxito", f"Consulta {consulta.id_consulta} actualizada a '{nuevo_estado}'")
            self.mostrar_menu_profesor()

    def interfaz_cancelar_consulta(self, consulta):
        self.limpiar_pantalla()
        tk.Label(self.root, text=f"Confirmar cancelación de la consulta {consulta.id_consulta}").pack()

        tk.Button(self.root, text="Confirmar", command=lambda: self.cancelar_consulta(consulta)).pack()
        tk.Button(self.root, text="Volver", command=self.mostrar_menu_profesor).pack()

    def cancelar_consulta(self, consulta):
        consulta.estado = "cancelada"
        messagebox.showinfo("Éxito", f"Consulta {consulta.id_consulta} ha sido cancelada")
        self.mostrar_menu_profesor()


    def guardar_nuevo_estado(self, consulta, nuevo_estado):
        consulta.estado = nuevo_estado
        messagebox.showinfo("Éxito", f"Consulta {consulta.id_consulta} actualizada a '{nuevo_estado}'")
        self.mostrar_menu_profesor()
       
    '''    
    def ver_horarios(self):
        
    def modificar_horario(self):
        
    def ver_notificaciones_profesor(self):
        
    def mostrar_horarios(self):
        
    def modificar_consulta(self):
    '''
    
    def ver_horarios(self):
        """Muestra los horarios registrados por el profesor."""
        self.limpiar_pantalla()
        tk.Label(self.root, text="Horarios Registrados:").pack()

        if not self.usuario_actual.horarios:
            tk.Label(self.root, text="No tiene horarios registrados").pack()
        else:
            for horario in self.usuario_actual.horarios:
                estado = "Disponible" if horario.disponible else "Ocupado"
                tk.Label(self.root, text=f"{horario.id_horario}: {horario.fecha}, {horario.hora_inicio}-{horario.hora_final} ({estado})").pack()

        tk.Button(self.root, text="Volver", command=self.mostrar_menu_profesor).pack()

    def modificar_horario(self):
        """Permite al profesor modificar uno de sus horarios registrados."""
        self.limpiar_pantalla()
        tk.Label(self.root, text="Seleccione un horario disponible:").pack()
        for horario in horarios:
            if horario.disponible:
                tk.Label(self.root, text=f"{horario.id_horario}: {horario.fecha} de {horario.hora_inicio} a {horario.hora_final}").pack()

        tk.Label(self.root, text="Ingrese ID del horario a modificar:").pack()
        self.id_horario_modificar_entry = tk.Entry(self.root)
        self.id_horario_modificar_entry.pack()
        tk.Button(self.root, text="Modificar", command=self.interfaz_modificar_horario).pack()
        tk.Button(self.root, text="Volver", command=self.mostrar_menu_profesor).pack()

    def interfaz_modificar_horario(self):
        """Muestra la interfaz para modificar los detalles de un horario específico."""
        id_horario = self.id_horario_modificar_entry.get()
        horario = next((h for h in self.usuario_actual.horarios if h.id_horario == id_horario), None)

        if horario:
            self.limpiar_pantalla()
            tk.Label(self.root, text=f"Modificando {horario.id_horario}").pack()

            tk.Label(self.root, text="Nueva Fecha (YYYY-MM-DD):").pack()
            nueva_fecha = tk.Entry(self.root)
            nueva_fecha.insert(0, horario.fecha)
            nueva_fecha.pack()

            tk.Label(self.root, text="Nueva Hora Inicio (HH:MM):").pack()
            nueva_hora_inicio = tk.Entry(self.root)
            nueva_hora_inicio.insert(0, horario.hora_inicio)
            nueva_hora_inicio.pack()

            tk.Label(self.root, text="Nueva Hora Final (HH:MM):").pack()
            nueva_hora_final = tk.Entry(self.root)
            nueva_hora_final.insert(0, horario.hora_final)
            nueva_hora_final.pack()

            tk.Button(self.root, text="Guardar Cambios", command=lambda: self.guardar_cambios_horario(horario, nueva_fecha.get(), nueva_hora_inicio.get(), nueva_hora_final.get())).pack()
            tk.Button(self.root, text="Volver", command=self.mostrar_menu_profesor).pack()
        else:
            messagebox.showerror("Error", "ID de horario no encontrado")
            self.mostrar_menu_profesor()

    def guardar_cambios_horario(self, horario, nueva_fecha, nueva_hora_inicio, nueva_hora_final):
        """Guarda los cambios realizados a un horario específico."""
        horario.fecha = nueva_fecha
        horario.hora_inicio = nueva_hora_inicio
        horario.hora_final = nueva_hora_final
        messagebox.showinfo("Éxito", f"Horario {horario.id_horario} modificado con éxito")
        self.mostrar_menu_profesor()

    def ver_notificaciones_profesor(self):
        """Muestra las notificaciones de consultas para el profesor."""
        self.limpiar_pantalla()
        tk.Label(self.root, text="Notificaciones de Consultas:").pack()

        consultas_asociadas = [c for c in consultas if c.profesor == self.usuario_actual.nombre]
        if not consultas_asociadas:
            tk.Label(self.root, text="No hay notificaciones").pack()
        else:
            for consulta in consultas_asociadas:
                tk.Label(self.root, text=f"Consulta {consulta.id_consulta}: {consulta.estado}").pack()

        tk.Button(self.root, text="Volver", command=self.mostrar_menu_profesor).pack()

    def mostrar_horarios(self):
        """Muestra los horarios disponibles para los estudiantes."""
        self.limpiar_pantalla()
        tk.Label(self.root, text="Horarios Disponibles:").pack()

        horarios_disponibles = [h for h in horarios if h.disponible]
        if not horarios_disponibles:
            tk.Label(self.root, text="No hay horarios disponibles").pack()
        else:
            for horario in horarios_disponibles:
                tk.Label(self.root, text=f"{horario.id_horario}: {horario.fecha} de {horario.hora_inicio} a {horario.hora_final}").pack()

        tk.Button(self.root, text="Volver", command=self.mostrar_menu_estudiante).pack()

    def modificar_consulta(self):
        """Permite al estudiante modificar o cancelar una consulta."""
        self.limpiar_pantalla()
        tk.Label(self.root, text="Gestión de Consultas:").pack()
        for consulta in consultas:
            if consulta.alumno == self.usuario_actual.nombre:
                tk.Label(self.root, text=f"Consulta {consulta.id_consulta} - Estado: {consulta.estado}").pack()
        
        tk.Label(self.root, text="Ingrese ID de la consulta a modificar o cancelar:").pack()
        self.id_consulta_modificar_entry = tk.Entry(self.root)
        self.id_consulta_modificar_entry.pack()
        tk.Button(self.root, text="Continuar", command=self.interfaz_modificar_consulta).pack()
        tk.Button(self.root, text="Volver", command=self.mostrar_menu_estudiante).pack()

    def interfaz_modificar_consulta(self):
        """Interfaz para modificar o cancelar una consulta."""
        id_consulta = self.id_consulta_modificar_entry.get()
        consulta = next((c for c in self.usuario_actual.consultas if c.id_consulta == id_consulta), None)

        if consulta:
            self.limpiar_pantalla()
            tk.Label(self.root, text=f"Modificando Consulta {consulta.id_consulta}").pack()

            if consulta.estado == "aprobar":
                tk.Label(self.root, text="Cancelar la consulta:").pack()
                tk.Button(self.root, text="Confirmar Cancelación", command=lambda: self.cancelar_consulta(consulta)).pack()
            else:
                tk.Label(self.root, text="Modificaciones permitidas solo para consultas aprobadas.").pack()

            tk.Button(self.root, text="Volver", command=self.mostrar_menu_estudiante).pack()
        else:
            messagebox.showerror("Error", "ID de consulta no encontrado")
            self.mostrar_menu_estudiante()


    def limpiar_pantalla(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# ------------------------ Ejecución del Programa ------------------------

if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaConsultas(root)
    root.mainloop()
