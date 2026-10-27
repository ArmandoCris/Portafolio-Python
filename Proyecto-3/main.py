import customtkinter as ctk
import sqlite3

class ExpenseTrackerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Expense Tracker")
        self.geometry("500x700")
        ctk.set_appearance_mode("dark")

        # Inicializar base de datos y UI
        self.init_db()
        self.create_widgets()
        self.cargar_datos()

    def init_db(self):
        """Conecta a SQLite y crea la tabla si no existe."""
        self.conn = sqlite3.connect("gastos.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS transacciones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo TEXT,
                monto REAL,
                descripcion TEXT
            )
        ''')
        self.conn.commit()

    def create_widgets(self):
        """Crea todos los elementos visuales de la interfaz."""
        # 1. Marco de Estadísticas (Top)
        self.stats_frame = ctk.CTkFrame(self)
        self.stats_frame.pack(pady=10, padx=20, fill="x")

        self.lbl_ingresos = ctk.CTkLabel(self.stats_frame, text="Total Ingresos: $0.00", text_color="#2ECC71", font=("Arial", 16, "bold"))
        self.lbl_ingresos.pack(pady=5)

        self.lbl_gastos = ctk.CTkLabel(self.stats_frame, text="Total Gastos: $0.00", text_color="#E74C3C", font=("Arial", 16, "bold"))
        self.lbl_gastos.pack(pady=5)

        self.lbl_balance = ctk.CTkLabel(self.stats_frame, text="Balance: $0.00", font=("Arial", 20, "bold"))
        self.lbl_balance.pack(pady=10)

        # 2. Marco del Formulario (Centro)
        self.form_frame = ctk.CTkFrame(self)
        self.form_frame.pack(pady=10, padx=20, fill="x")

        self.tipo_var = ctk.StringVar(value="Gasto")
        self.tipo_menu = ctk.CTkOptionMenu(self.form_frame, variable=self.tipo_var, values=["Ingreso", "Gasto"])
        self.tipo_menu.pack(pady=10, padx=10, fill="x")

        self.monto_entry = ctk.CTkEntry(self.form_frame, placeholder_text="Monto (ej. 50000)")
        self.monto_entry.pack(pady=10, padx=10, fill="x")

        self.desc_entry = ctk.CTkEntry(self.form_frame, placeholder_text="Descripción del movimiento")
        self.desc_entry.pack(pady=10, padx=10, fill="x")

        self.btn_agregar = ctk.CTkButton(self.form_frame, text="Agregar Transacción", command=self.agregar_transaccion)
        self.btn_agregar.pack(pady=15, padx=10, fill="x")

        # 3. Marco del Historial (Fondo)
        self.historial_frame = ctk.CTkScrollableFrame(self, label_text="Historial de Transacciones")
        self.historial_frame.pack(pady=10, padx=20, fill="both", expand=True)

    def agregar_transaccion(self):
        """Captura los datos, los guarda en SQLite y actualiza la pantalla."""
        tipo = self.tipo_var.get()
        monto_texto = self.monto_entry.get().strip()
        descripcion = self.desc_entry.get().strip()

        # Validación simple para asegurar que el monto es un número
        try:
            monto = float(monto_texto)
        except ValueError:
            return  # Si no es un número, se ignora el clic por ahora

        if not descripcion:
            return

        # Insertar en base de datos
        self.cursor.execute("INSERT INTO transacciones (tipo, monto, descripcion) VALUES (?, ?, ?)", (tipo, monto, descripcion))
        self.conn.commit()

        # Limpiar los campos de texto
        self.monto_entry.delete(0, 'end')
        self.desc_entry.delete(0, 'end')

        # Recargar la interfaz
        self.cargar_datos()

    def cargar_datos(self):
        """Consulta la base de datos, calcula estadísticas y dibuja el historial."""
        # Limpiar el historial visual actual
        for widget in self.historial_frame.winfo_children():
            widget.destroy()

        self.cursor.execute("SELECT tipo, monto, descripcion FROM transacciones ORDER BY id DESC")
        transacciones = self.cursor.fetchall()

        total_ingresos = 0.0
        total_gastos = 0.0

        for tipo, monto, descripcion in transacciones:
            # Calcular totales
            if tipo == "Ingreso":
                total_ingresos += monto
                color = "#2ECC71"  # Verde
            else:
                total_gastos += monto
                color = "#E74C3C"  # Rojo

            # Dibujar cada fila en el historial
            texto_fila = f"{tipo}: ${monto:,.2f} - {descripcion}"
            fila_label = ctk.CTkLabel(self.historial_frame, text=texto_fila, text_color=color, anchor="w", font=("Arial", 12))
            fila_label.pack(fill="x", padx=5, pady=2)

        # Actualizar las etiquetas superiores
        balance = total_ingresos - total_gastos
        
        self.lbl_ingresos.configure(text=f"Total Ingresos: ${total_ingresos:,.2f}")
        self.lbl_gastos.configure(text=f"Total Gastos: ${total_gastos:,.2f}")
        self.lbl_balance.configure(text=f"Balance: ${balance:,.2f}")

if __name__ == "__main__":
    app = ExpenseTrackerApp()
    app.mainloop()