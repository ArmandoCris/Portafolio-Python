import customtkinter as ctk
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class FinanceDashboardApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Dashboard de Finanzas")
        self.geometry("800x600")
        ctk.set_appearance_mode("dark")

        # Interceptar el cierre de la ventana para apagar limpiamente los procesos
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.init_db()
        self.create_widgets()
        self.cargar_datos()

    def init_db(self):
        self.conn = sqlite3.connect("finanzas.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS movimientos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                mes TEXT,
                tipo TEXT,
                categoria TEXT,
                monto REAL
            )
        ''')
        self.conn.commit()
        self.inyectar_datos_prueba()

    def inyectar_datos_prueba(self):
        """Inyecta datos ficticios solo si la base de datos está vacía."""
        self.cursor.execute("SELECT COUNT(*) FROM movimientos")
        if self.cursor.fetchone()[0] == 0:
            datos = [
                ("Octubre", "Ingreso", "Salario", 3500.0),
                ("Octubre", "Gasto", "Alquiler", 1200.0),
                ("Octubre", "Gasto", "Comida", 450.0),
                ("Octubre", "Gasto", "Transporte", 150.0),
                ("Octubre", "Gasto", "Entretenimiento", 200.0)
            ]
            self.cursor.executemany("INSERT INTO movimientos (mes, tipo, categoria, monto) VALUES (?, ?, ?, ?)", datos)
            self.conn.commit()

    def create_widgets(self):
        # Panel superior (KPIs)
        self.kpi_frame = ctk.CTkFrame(self)
        self.kpi_frame.pack(fill="x", padx=20, pady=20)

        self.lbl_ingresos = ctk.CTkLabel(self.kpi_frame, text="Total Ingresos: $0", font=("Arial", 16, "bold"), text_color="#2ECC71")
        self.lbl_ingresos.pack(side="left", expand=True, pady=10)

        self.lbl_gastos = ctk.CTkLabel(self.kpi_frame, text="Total Gastos: $0", font=("Arial", 16, "bold"), text_color="#E74C3C")
        self.lbl_gastos.pack(side="left", expand=True, pady=10)

        self.lbl_saldo = ctk.CTkLabel(self.kpi_frame, text="Saldo Neto: $0", font=("Arial", 16, "bold"))
        self.lbl_saldo.pack(side="left", expand=True, pady=10)

        # Panel inferior (Lienzo del Gráfico)
        self.chart_frame = ctk.CTkFrame(self)
        self.chart_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    def cargar_datos(self):
        self.cursor.execute("SELECT tipo, categoria, monto FROM movimientos")
        movimientos = self.cursor.fetchall()

        total_ingresos = sum(m[2] for m in movimientos if m[0] == "Ingreso")
        total_gastos = sum(m[2] for m in movimientos if m[0] == "Gasto")
        saldo = total_ingresos - total_gastos

        self.lbl_ingresos.configure(text=f"Total Ingresos: ${total_ingresos:,.2f}")
        self.lbl_gastos.configure(text=f"Total Gastos: ${total_gastos:,.2f}")
        self.lbl_saldo.configure(text=f"Saldo Neto: ${saldo:,.2f}")

        # Preparar datos para el gráfico de Dona
        gastos_cat = {}
        for m in movimientos:
            if m[0] == "Gasto":
                gastos_cat[m[1]] = gastos_cat.get(m[1], 0) + m[2]

        categorias = list(gastos_cat.keys())
        montos = list(gastos_cat.values())

        # Configuración del gráfico de Dona
        fig, ax = plt.subplots(figsize=(6, 4), facecolor='#242424')
        colores = ['#E74C3C', '#3498DB', '#F1C40F', '#9B59B6', '#1ABC9C']
        
        wedges, texts, autotexts = ax.pie(
            montos, 
            labels=categorias, 
            autopct='%1.1f%%', 
            startangle=140, 
            colors=colores,
            textprops=dict(color="w", fontsize=10),
            wedgeprops=dict(width=0.4, edgecolor='#242424', linewidth=2)
        )
        
        ax.set_title("Distribución de Gastos", color='white', pad=15, fontdict={'fontsize': 14, 'fontweight': 'bold'})

        # Limpiar lienzo anterior si existiera y renderizar
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
            
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

    def on_closing(self):
        """Apaga los procesos en segundo plano y cierra la app limpiamente."""
        plt.close('all')  # Libera la memoria del motor de Matplotlib
        self.quit()       # Detiene el ciclo principal (mainloop)
        self.destroy()    # Destruye los widgets de CustomTkinter

if __name__ == "__main__":
    app = FinanceDashboardApp()
    app.mainloop()