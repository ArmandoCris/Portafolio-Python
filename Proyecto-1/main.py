import customtkinter as ctk
import sqlite3

class ToDoApp(ctk.CTk):
    """
    Clase principal para la aplicación de tareas (To-Do App).
    Hereda de customtkinter.CTk y define la interfaz gráfica base.
    """

    def __init__(self):
        super().__init__()

        # Configuración de la ventana principal
        self.title("To-Do App")
        self.geometry("500x600")
        self.resizable(False, False)
        ctk.set_appearance_mode("dark")  # Tema oscuro por defecto

        # Conexión a la base de datos
        self.db_connection = self.connect_to_db()

        # Crear widgets de la interfaz
        self.create_widgets()

        # Leer y renderizar tareas desde la base de datos
        self.read_tasks()

    def connect_to_db(self):
        """
        Método para conectarse a la base de datos SQLite.
        Crea la tabla 'tareas' si no existe.
        """
        conn = sqlite3.connect("todo.db")
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tareas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                descripcion TEXT NOT NULL,
                completada INTEGER DEFAULT 0
            )
        """)
        conn.commit()
        return conn

    def create_widgets(self):
        """
        Método para crear y organizar los widgets de la interfaz gráfica.
        """
        # Campo de entrada de texto para nuevas tareas
        self.task_entry = ctk.CTkEntry(self, placeholder_text="Escribe una nueva tarea")
        self.task_entry.pack(pady=10, padx=10, fill="x")

        # Botón para agregar tareas
        self.add_task_button = ctk.CTkButton(self, text="Agregar Tarea", command=self.add_task)
        self.add_task_button.pack(pady=10, padx=10)

        # Marco desplazable para listar las tareas
        self.task_frame = ctk.CTkScrollableFrame(self)
        self.task_frame.pack(pady=10, padx=10, fill="both", expand=True)

    def read_tasks(self):
        """
        Método para leer las tareas desde la base de datos y renderizarlas en la interfaz.
        """
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT id, descripcion, completada FROM tareas")
        tasks = cursor.fetchall()

        for task in tasks:
            self.render_task(task[0], task[1], task[2])

    def add_task(self):
        """
        Método para agregar una nueva tarea a la base de datos y renderizarla.
        """
        task_text = self.task_entry.get().strip()
        if task_text:  # Verificar que el campo no esté vacío
            cursor = self.db_connection.cursor()
            cursor.execute("INSERT INTO tareas (descripcion) VALUES (?)", (task_text,))
            self.db_connection.commit()

            task_id = cursor.lastrowid
            self.render_task(task_id, task_text, 0)

            # Limpiar el campo de entrada
            self.task_entry.delete(0, "end")

    def render_task(self, task_id, description, completed):
        """
        Método para renderizar una tarea en el marco desplazable.
        """
        task_frame = ctk.CTkFrame(self.task_frame)
        task_frame.pack(pady=5, padx=5, fill="x")

        # Checkbox para marcar la tarea como completada
        task_checkbox = ctk.CTkCheckBox(
            task_frame,
            text=description,
            command=lambda: self.update_task_status(task_id, task_checkbox.get())
        )
        task_checkbox.pack(side="left", padx=10)
        task_checkbox.select() if completed else task_checkbox.deselect()

        # Botón para eliminar la tarea
        delete_button = ctk.CTkButton(
            task_frame,
            text="Eliminar",
            command=lambda: self.delete_task(task_id, task_frame)
        )
        delete_button.pack(side="right", padx=10)

    def update_task_status(self, task_id, status):
        """
        Método para actualizar el estado de completada de una tarea en la base de datos.
        """
        cursor = self.db_connection.cursor()
        cursor.execute("UPDATE tareas SET completada = ? WHERE id = ?", (status, task_id))
        self.db_connection.commit()

    def delete_task(self, task_id, task_frame):
        """
        Método para eliminar una tarea de la base de datos y de la interfaz.
        """
        cursor = self.db_connection.cursor()
        cursor.execute("DELETE FROM tareas WHERE id = ?", (task_id,))
        self.db_connection.commit()

        # Eliminar el frame de la tarea de la interfaz
        task_frame.destroy()

if __name__ == "__main__":
    app = ToDoApp()
    app.mainloop()