import tkinter as tk
from tkinter import messagebox, simpledialog
from datetime import datetime, timedelta

# Clase Usuario
class Usuario:
    def __init__(self, nombre, correo, clave, contrasena):
        self.nombre = nombre
        self.correo = correo
        self.clave = clave
        self.contrasena = contrasena

    def inicio_sesion(self, clave, contrasena):
        if self.clave == clave and self.contrasena == contrasena:
            return True
        return False
    
class Consulta:
    def __init__(self, id, fecha, hora_inicio, hora_fin, nombreAlumno, nombreProfesor, estado):
        self.id = id
        self.fecha = fecha
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin
        self.nombreAlumno = nombreAlumno
        self.nombreProfesor = nombreProfesor
        self.estado = estado
        self.notificaciones = []
        
    def cambiar_estado(self, nuevo_estado):
        """Cambia el estado de la consulta y genera una notificación."""
        self.estado = nuevo_estado
        notificacion = f"Consulta {self.id} | {self.profesor} | Estado: {self.estado} | Fecha: {self.fecha.strftime('%Y-%m-%d %H:%M:%S')}"
        self.notificaciones.append(notificacion)

# Clase Alumno (hereda de Usuario)
class Alumno(Usuario):
    def __init__(self, nombre, correo, clave, contrasena):
        super().__init__(nombre, correo, clave, contrasena)
        self.consultas = []
        self.notificaciones = [] 

    def solicitar_consulta(self, horario_id, duracion, horarios_disponibles):
        # Buscar el horario por ID
        horario = next((h for h in horarios_disponibles if h.id == horario_id), None)
        
        if not horario:
            return "Horario no encontrado"
        
        if horario.disponibilidad == "Disponible":
            # Crear la consulta con la duración seleccionada
            hora_fin = horario.hora_inicio + timedelta(minutes=duracion)
            consulta = Consulta(len(self.consultas) + 1, horario.fecha, horario.hora_inicio, hora_fin, self.nombre, horario.nombreProfesor, "solicitud")
            self.consultas.append(consulta)
            # Actualizar la disponibilidad del horario
            horario.disponibilidad = "No Disponible"
            return "Consulta solicitada con éxito"
        return "El horario no está disponible"
    
    def modificar_o_cancelar_consulta(self, consulta_id, nueva_hora_inicio=None, nueva_hora_fin=None):
        consulta = next((c for c in self.consultas if c.id == consulta_id), None)
        
        if not consulta:
            return "Consulta no encontrada"
        
        if consulta.estado == "solicitud" or consulta.estado == "aprobada" or consulta.estado == "rechazada":
            if nueva_hora_inicio and nueva_hora_fin:
                if self.validar_modificacion(consulta, nueva_hora_inicio, nueva_hora_fin):
                    consulta.hora_inicio = nueva_hora_inicio
                    consulta.hora_fin = nueva_hora_fin
                    consulta.estado = "solicitud"  # Reiniciar a estado "solicitud"
                    self.actualizar_notificaciones(consulta, "modificada")
                    self.actualizar_horarios(consulta)
                    return "Consulta modificada exitosamente"
            elif nueva_hora_inicio is None and nueva_hora_fin is None:
                # Cancelar consulta
                consulta.estado = "cancelada"
                self.eliminar_de_horarios(consulta)
                self.actualizar_notificaciones(consulta, "cancelada")
                return "Consulta cancelada exitosamente"
            else:
                return "Error: Si se desea modificar la consulta, ambos horarios deben ser proporcionados"
        else:
            return "La consulta no puede ser modificada o cancelada en su estado actual"

    def validar_modificacion(self, consulta, nueva_hora_inicio, nueva_hora_fin):
        if nueva_hora_inicio >= nueva_hora_fin:
            return False  # La duración debe ser mayor a 0
        for c in self.consultas:
            if c.estado != "cancelada" and not (nueva_hora_fin <= c.hora_inicio or nueva_hora_inicio >= c.hora_fin):
                return False  # Verificar solapamiento de horarios
        return True
    
# Clase Profesor (hereda de Usuario)
class Profesor(Usuario):
    def __init__(self, nombre, correo, clave, contrasena):
        super().__init__(nombre, correo, clave, contrasena)
        self.horarios = []
        self.consultas = []

    def registrar_horario(self, hora_inicio, hora_fin):
        # Verificar que el horario no se superponga con los horarios existentes
        for horario in self.horarios:
            if (hora_inicio < horario.hora_fin and hora_fin > horario.hora_inicio):
                return "Error: El horario se superpone con otro horario ya registrado."
        
        # Calcular la duración del horario
        duracion = (hora_fin - hora_inicio).seconds // 60
        
        # Crear un nuevo horario y agregarlo
        nuevo_horario = Horario(len(base_de_datos["horarios"]) + 1, datetime.now().date(), hora_inicio, hora_fin, self.nombre, "Disponible")
        self.horarios.append(nuevo_horario)
        base_de_datos["horarios"].append(nuevo_horario)  # Asegurarse de que el horario se guarde en la base de datos
        
        # Ahora incluimos la duración en el mensaje de confirmación
        return f"Horario registrado con éxito. Duración: {duracion} minutos."

    def ver_consultas(self):
        # Filtrar las consultas asociadas al profesor
        return [consulta for consulta in self.consultas if consulta.nombreProfesor == self.nombre]

    def cambiar_estado_consulta(self, consulta_id, nuevo_estado):
        # Buscar consulta por ID
        consulta = next((c for c in self.consultas if c.id == consulta_id), None)
        
        if not consulta:
            return "Consulta no encontrada"
        
        if consulta.estado == "solicitud" and nuevo_estado in ["aprobada", "rechazada"]:
            consulta.estado = nuevo_estado
            return f"Estado de consulta {consulta_id} cambiado a {nuevo_estado}"
        elif consulta.estado == "aprobada" and nuevo_estado == "cancelada":
            # Verificar si la consulta aún no ha ocurrido
            if consulta.fecha > datetime.now().date():
                consulta.estado = nuevo_estado
                return f"Consulta {consulta_id} cancelada"
            else:
                return "No se puede cancelar una consulta ya pasada"
        else:
            return "Operación no permitida en este estado"

# Clase Horario
class Horario:
    def __init__(self, id, fecha, hora_inicio, hora_fin, nombreProfesor, disponibilidad):
        self.id = id
        self.fecha = fecha
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin
        self.duracion = (hora_fin - hora_inicio).seconds // 60
        self.nombreProfesor = nombreProfesor
        self.disponibilidad = disponibilidad

# Base de Datos (diccionario)
base_de_datos = {
    "usuarios": {
        "profesor@dominio.com": Profesor("Profesor Uno", "profesor@dominio.com", 12345, "123"),
        "alumno@dominio.com": Alumno("Alumno Uno", "alumno@dominio.com", 54321, "321")
    },
    "horarios": [],
    "consultas": []
}

# Funciones de Interfaz con Tkinter
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión de Consultas")
        
        # Crear una ventana de inicio de sesión
        self.frame_login = tk.Frame(self.root)
        self.frame_login.pack(padx=10, pady=10)

        self.label_email = tk.Label(self.frame_login, text="Correo Electrónico:")
        self.label_email.grid(row=0, column=0, padx=5, pady=5)
        
        self.entry_email = tk.Entry(self.frame_login)
        self.entry_email.grid(row=0, column=1, padx=5, pady=5)

        self.label_pass = tk.Label(self.frame_login, text="Contraseña:")
        self.label_pass.grid(row=1, column=0, padx=5, pady=5)

        self.entry_pass = tk.Entry(self.frame_login, show="*")
        self.entry_pass.grid(row=1, column=1, padx=5, pady=5)

        self.btn_login = tk.Button(self.frame_login, text="Iniciar Sesión", command=self.iniciar_sesion)
        self.btn_login.grid(row=2, columnspan=2, pady=5)

    def iniciar_sesion(self):
        email = self.entry_email.get()
        contrasena = self.entry_pass.get()

        # Verificar si el usuario existe en la base de datos
        usuario = base_de_datos["usuarios"].get(email, None)
        if usuario and usuario.inicio_sesion(usuario.clave, contrasena):
            messagebox.showinfo("Éxito", f"Bienvenido {usuario.nombre}")
            # Redirigir según el tipo de usuario (Alumno o Profesor)
            self.mostrar_menu_usuario(usuario)
        else:
            messagebox.showerror("Error", "Correo o contraseña incorrectos")

    def mostrar_menu_usuario(self, usuario):
        # Limpiar la ventana de inicio de sesión
        for widget in self.frame_login.winfo_children():
            widget.destroy()

        # Mostrar el menú según el tipo de usuario
        if isinstance(usuario, Alumno):
            self.mostrar_menu_alumno(usuario)
        elif isinstance(usuario, Profesor):
            self.mostrar_menu_profesor(usuario)

    def mostrar_menu_alumno(self, alumno):
        label = tk.Label(self.root, text=f"Bienvenido, {alumno.nombre} (Alumno)", font=("Arial", 16))
        label.pack(pady=10)

        btn_solicitar = tk.Button(self.root, text="Solicitar Consulta", command=lambda: self.solicitar_consulta(alumno))
        btn_solicitar.pack(pady=5)
        
        btn_notificaciones = tk.Button(self.root, text="Ver Notificaciones", command=lambda: self.ver_notificaciones(alumno))
        btn_notificaciones.pack(pady=5)
        
        btn_modificar_cancelar = tk.Button(self.root, text="Modificar o Cancelar Consulta", command=lambda: self.modificar_o_cancelar_consulta(alumno))
        btn_modificar_cancelar.pack(pady=5)

        btn_logout = tk.Button(self.root, text="Cerrar Sesión", command=self.volver_a_inicio_sesion)
        btn_logout.pack(pady=5)

    def mostrar_menu_profesor(self, profesor):
        label = tk.Label(self.root, text=f"Bienvenido, {profesor.nombre} (Profesor)", font=("Arial", 16))
        label.pack(pady=10)

        btn_notificaciones = tk.Button(self.root, text="Ver Notificaciones", command=lambda: self.ver_notificaciones(profesor))
        btn_notificaciones.pack(pady=5)

        btn_ver_consultas = tk.Button(self.root, text="Ver Consultas", command=lambda: self.ver_consultas(profesor))
        btn_ver_consultas.pack(pady=5)
        
        btn_registrar_horario = tk.Button(self.root, text="Registrar Horario", command=lambda: self.registrar_horario(profesor))
        btn_registrar_horario.pack(pady=5)

        btn_ver_horarios = tk.Button(self.root, text="Ver Horarios Disponibles", command=lambda: self.ver_horarios_disponibles())
        btn_ver_horarios.pack(pady=5)
        
        btn_modificar_horario = tk.Button(self.root, text="Modificar Horario", command=lambda: self.modificar_horario(profesor))
        btn_modificar_horario.pack(pady=5)

        btn_logout = tk.Button(self.root, text="Cerrar Sesión", command=self.volver_a_inicio_sesion)
        btn_logout.pack(pady=5)
        
    def ver_horarios_disponibles(self):
        horarios_disponibles = [h for h in base_de_datos["horarios"] if h.disponibilidad == "Disponible"]
        
        if not horarios_disponibles:
            messagebox.showinfo("Horarios Disponibles", "No hay horarios disponibles.")
            return
        
        horario_str = "\n".join([f"ID: {h.id} | {h.hora_inicio.strftime('%H:%M')} - {h.hora_fin.strftime('%H:%M')} | Profesor: {h.nombreProfesor}" for h in horarios_disponibles])
        
        messagebox.showinfo("Horarios Disponibles", f"Horarios disponibles:\n{horario_str}")
        
    def registrar_horario(self, profesor):
        # Solicitar la hora de inicio y fin del horario
        hora_inicio_str = simpledialog.askstring("Hora de Inicio", "Ingrese la hora de inicio (formato HH:MM):")
        hora_fin_str = simpledialog.askstring("Hora de Fin", "Ingrese la hora de fin (formato HH:MM):")
        
        try:
            hora_inicio = datetime.strptime(hora_inicio_str, "%H:%M")
            hora_fin = datetime.strptime(hora_fin_str, "%H:%M")
            
            if hora_inicio >= hora_fin:
                messagebox.showerror("Error", "La hora de inicio debe ser anterior a la hora de finalización.")
                return
            
            # Registrar el horario en el sistema
            mensaje = profesor.registrar_horario(hora_inicio, hora_fin)
            messagebox.showinfo("Resultado", mensaje)
        
        except ValueError:
            messagebox.showerror("Error", "Formato de hora inválido. Por favor, use el formato HH:MM.")
            
    def modificar_horario(self, profesor):
        # Verificar si el profesor tiene horarios registrados
        if not profesor.horarios:
            messagebox.showinfo("Modificar Horario", "No hay horarios registrados para modificar.")
            return
        
        # Mostrar los horarios registrados
        horario_str = "\n".join([f"ID: {h.id} | Inicio: {h.hora_inicio.strftime('%H:%M')} - Fin: {h.hora_fin.strftime('%H:%M')}" for h in profesor.horarios])
        
        # Pedir al profesor que seleccione el ID del horario que quiere modificar
        horario_id = simpledialog.askinteger("Seleccionar Horario", f"Horarios registrados:\n{horario_str}\nSeleccione el ID del horario a modificar:")
        
        if horario_id:
            # Llamar al método de la clase Profesor para modificar el horario
            mensaje = profesor.modificar_horario()
            messagebox.showinfo("Resultado de Modificación", mensaje)

    def solicitar_consulta(self, alumno):
        # Mostrar horarios disponibles
        horarios_disponibles = [h for h in base_de_datos["horarios"] if h.disponibilidad == "Disponible"]
        
        if not horarios_disponibles:
            messagebox.showinfo("Consulta", "No hay horarios disponibles.")
            return
        
        horario_str = "\n".join([f"ID: {h.id} | {h.hora_inicio.strftime('%H:%M')} - {h.hora_fin.strftime('%H:%M')} | Profesor: {h.nombreProfesor}" for h in horarios_disponibles])
        
        # Pedir al alumno que seleccione un horario
        id_horario = simpledialog.askinteger("Seleccionar Horario", f"Horarios disponibles:\n{horario_str}\nSeleccione el ID del horario:")
        
        if id_horario:
            duracion = simpledialog.askinteger("Duración", "¿Cuántos minutos durará la consulta?")
            
            mensaje = alumno.solicitar_consulta(id_horario, duracion, horarios_disponibles)
            messagebox.showinfo("Resultado de Solicitud", mensaje)
            
    def ver_notificaciones(self, usuario):
        """Muestra las notificaciones relacionadas con el usuario (Alumno o Profesor)."""
        if isinstance(usuario, Alumno):
            # Filtramos las notificaciones del alumno
            notificaciones = [consulta.notificaciones for consulta in base_de_datos["consultas"] if consulta.alumno == usuario]
        elif isinstance(usuario, Profesor):
            # Filtramos las notificaciones del profesor
            notificaciones = [consulta.notificaciones for consulta in base_de_datos["consultas"] if consulta.profesor == usuario]

        if not notificaciones:
            messagebox.showinfo("Notificaciones", "No hay notificaciones disponibles.")
            return

        # Mostramos las notificaciones
        notificaciones_str = "\n".join([f"ID: {consulta.id} | Hora: {consulta.fecha.strftime('%H:%M')} | Estado: {consulta.estado}" for consulta in notificaciones])
        messagebox.showinfo("Notificaciones", f"Notificaciones:\n{notificaciones_str}")

    def ver_consultas(self, profesor):
        consultas = profesor.ver_consultas()
        if not consultas:
            messagebox.showinfo("Consultas", "No hay consultas asociadas.")
            return

        # Mostrar las consultas del profesor
        consulta_str = "\n".join([f"ID: {c.id} | Alumno: {c.nombreAlumno} | Estado: {c.estado}" for c in consultas])
        
        # Pedir al profesor que seleccione una consulta para cambiar su estado
        consulta_id = simpledialog.askinteger("Seleccionar Consulta", f"Consultas:\n{consulta_str}\nSeleccione el ID de la consulta:")
        if consulta_id:
            nuevo_estado = simpledialog.askstring("Nuevo Estado", "Ingrese el nuevo estado (aprobada, rechazada, cancelada):")
            mensaje = profesor.cambiar_estado_consulta(consulta_id, nuevo_estado)
            messagebox.showinfo("Resultado de Cambio de Estado", mensaje)
            
    def modificar_o_cancelar_consulta(self, alumno):
        # Mostrar las consultas del alumno
        consultas = [consulta for consulta in base_de_datos["consultas"] if consulta.alumno == alumno]
        
        if not consultas:
            messagebox.showinfo("Modificar/Cancelar Consulta", "No tienes consultas registradas.")
            return

        consulta_str = "\n".join([f"ID: {c.id} | Hora: {c.fecha.strftime('%H:%M')} | Estado: {c.estado}" for c in consultas])
        
        # Pedir al alumno que seleccione una consulta
        consulta_id = simpledialog.askinteger("Seleccionar Consulta", f"Consultas:\n{consulta_str}\nSeleccione el ID de la consulta:")
        
        if consulta_id:
            # Buscar la consulta en base de datos
            consulta = next((c for c in consultas if c.id == consulta_id), None)
            if consulta:
                # Confirmar si desea modificar o cancelar
                accion = simpledialog.askstring("Acción", "Ingrese 'modificar' para modificar o 'cancelar' para cancelar la consulta:")
                
                if accion == "modificar":
                    # Lógica para modificar consulta
                    nuevo_horario = simpledialog.askstring("Nuevo Horario", "Ingrese el nuevo horario de la consulta (formato HH:MM):")
                    mensaje = alumno.modificar_consulta(consulta_id, nuevo_horario)
                    messagebox.showinfo("Resultado de Modificación", mensaje)
                elif accion == "cancelar":
                    # Lógica para cancelar consulta
                    mensaje = alumno.cancelar_consulta(consulta_id)
                    messagebox.showinfo("Resultado de Cancelación", mensaje)
                else:
                    messagebox.showerror("Error", "Acción no válida.")
            else:
                messagebox.showerror("Error", "Consulta no encontrada.")
    

    def volver_a_inicio_sesion(self):
        # Limpiar la ventana actual y volver a la pantalla de inicio de sesión
        for widget in self.root.winfo_children():
            widget.destroy()
        self.__init__(self.root)

# Ejecutar la aplicación
root = tk.Tk()
app = App(root)
root.mainloop()

