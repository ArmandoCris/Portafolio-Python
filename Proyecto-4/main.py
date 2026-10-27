import customtkinter as ctk
import sqlite3
import random
import string
import pyperclip

class URLShortenerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("URL Shortener Local")
        self.geometry("550x600")
        ctk.set_appearance_mode("dark")

        self.init_db()
        self.create_widgets()
        self.cargar_historial()

    def init_db(self):
        """Conecta a SQLite y crea la tabla si no existe."""
        self.conn = sqlite3.connect("urls.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS enlaces (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url_original TEXT,
                codigo_corto TEXT,
                clics INTEGER DEFAULT 0
            )
        ''')
        self.conn.commit()

    def create_widgets(self):
        """Crea los elementos visuales de la interfaz."""
        # Formulario superior
        self.form_frame = ctk.CTkFrame(self)
        self.form_frame.pack(pady=20, padx=20, fill="x")

        self.url_entry = ctk.CTkEntry(self.form_frame, placeholder_text="Ingresa la URL original (ej. https://github.com/...)")
        self.url_entry.pack(pady=10, padx=10, fill="x")

        self.btn_acortar = ctk.CTkButton(self.form_frame, text="Acortar URL", command=self.acortar_url)
        self.btn_acortar.pack(pady=10, padx=10)

        # Marco del historial inferior
        self.historial_frame = ctk.CTkScrollableFrame(self, label_text="Historial de Enlaces")
        self.historial_frame.pack(pady=10, padx=20, fill="both", expand=True)

    def acortar_url(self):
        """Genera el código corto, guarda en base de datos y actualiza."""
        url_original = self.url_entry.get().strip()
        if not url_original:
            return

        # Generar código alfanumérico aleatorio de 6 caracteres
        caracteres = string.ascii_letters + string.digits
        codigo_corto = ''.join(random.choices(caracteres, k=6))

        # Insertar registro inicial con 0 clics
        self.cursor.execute("INSERT INTO enlaces (url_original, codigo_corto) VALUES (?, ?)", (url_original, codigo_corto))
        self.conn.commit()

        self.url_entry.delete(0, 'end')
        self.cargar_historial()

    def copiar_y_usar(self, id_enlace, codigo_corto):
        """Suma un uso (clic) a la base de datos y copia al portapapeles."""
        # Incrementar contador en SQLite
        self.cursor.execute("UPDATE enlaces SET clics = clics + 1 WHERE id = ?", (id_enlace,))
        self.conn.commit()

        # Simular un dominio de acortador y copiar usando pyperclip
        url_simulada = f"http://sh.ort/{codigo_corto}"
        pyperclip.copy(url_simulada)

        # Recargar para mostrar el nuevo número de clics
        self.cargar_historial()

    def cargar_historial(self):
        """Consulta los enlaces guardados y los dibuja en la pantalla."""
        # Limpiar filas existentes antes de recargar
        for widget in self.historial_frame.winfo_children():
            widget.destroy()

        self.cursor.execute("SELECT id, url_original, codigo_corto, clics FROM enlaces ORDER BY id DESC")
        enlaces = self.cursor.fetchall()

        for id_enlace, original, corto, clics in enlaces:
            # Contenedor horizontal para cada registro
            fila = ctk.CTkFrame(self.historial_frame)
            fila.pack(fill="x", pady=5, padx=5)

            # Truncar visualmente la URL original si es muy larga
            url_display = original[:30] + "..." if len(original) > 30 else original
            texto_info = f"{url_display}  ->  {corto}  |  Clics: {clics}"

            lbl_info = ctk.CTkLabel(fila, text=texto_info, anchor="w", font=("Arial", 12))
            lbl_info.pack(side="left", padx=10, pady=10)

            # El uso de lambda permite pasar argumentos específicos a la función del botón
            btn_copiar = ctk.CTkButton(fila, text="Copiar", width=60, 
                                       command=lambda i=id_enlace, c=corto: self.copiar_y_usar(i, c))
            btn_copiar.pack(side="right", padx=10, pady=10)

if __name__ == "__main__":
    app = URLShortenerApp()
    app.mainloop()