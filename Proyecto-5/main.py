import customtkinter as ctk
import sqlite3
import bcrypt
import jwt

SECRET_KEY = "clave_secreta_para_jwt"

class AuthApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Autenticación")
        self.geometry("400x500")
        ctk.set_appearance_mode("dark")

        self.init_db()
        
        # Contenedores de las pantallas (Frames)
        self.login_frame = ctk.CTkFrame(self)
        self.register_frame = ctk.CTkFrame(self)
        self.dashboard_frame = ctk.CTkFrame(self)

        self.build_login()
        self.build_register()
        self.build_dashboard()

        # Mostrar login por defecto al abrir la app
        self.show_frame(self.login_frame)

    def init_db(self):
        self.conn = sqlite3.connect("usuarios.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                correo TEXT UNIQUE,
                password_hash BLOB
            )
        ''')
        self.conn.commit()

    def show_frame(self, frame_to_show):
        """Oculta todos los marcos y muestra solo el solicitado."""
        self.login_frame.pack_forget()
        self.register_frame.pack_forget()
        self.dashboard_frame.pack_forget()
        frame_to_show.pack(fill="both", expand=True, padx=20, pady=20)

    def build_login(self):
        ctk.CTkLabel(self.login_frame, text="Iniciar Sesión", font=("Arial", 24, "bold")).pack(pady=20)
        self.entry_login_email = ctk.CTkEntry(self.login_frame, placeholder_text="Correo electrónico")
        self.entry_login_email.pack(pady=10, fill="x", padx=20)
        
        self.entry_login_pass = ctk.CTkEntry(self.login_frame, placeholder_text="Contraseña", show="*")
        self.entry_login_pass.pack(pady=10, fill="x", padx=20)
        
        self.lbl_login_msg = ctk.CTkLabel(self.login_frame, text="", text_color="red")
        self.lbl_login_msg.pack()

        ctk.CTkButton(self.login_frame, text="Ingresar", command=self.login).pack(pady=10)
        ctk.CTkButton(self.login_frame, text="Crear Cuenta", fg_color="transparent", border_width=1, 
                      command=lambda: self.show_frame(self.register_frame)).pack(pady=5)

    def build_register(self):
        ctk.CTkLabel(self.register_frame, text="Registro", font=("Arial", 24, "bold")).pack(pady=20)
        self.entry_reg_email = ctk.CTkEntry(self.register_frame, placeholder_text="Correo electrónico")
        self.entry_reg_email.pack(pady=10, fill="x", padx=20)
        
        self.entry_reg_pass = ctk.CTkEntry(self.register_frame, placeholder_text="Contraseña", show="*")
        self.entry_reg_pass.pack(pady=10, fill="x", padx=20)
        
        self.lbl_reg_msg = ctk.CTkLabel(self.register_frame, text="", text_color="red")
        self.lbl_reg_msg.pack()

        ctk.CTkButton(self.register_frame, text="Registrar", command=self.register).pack(pady=10)
        ctk.CTkButton(self.register_frame, text="Volver al Login", fg_color="transparent", 
                      command=lambda: self.show_frame(self.login_frame)).pack(pady=5)

    def build_dashboard(self):
        ctk.CTkLabel(self.dashboard_frame, text="Área Privada", font=("Arial", 24, "bold")).pack(pady=20)
        ctk.CTkLabel(self.dashboard_frame, text="Token JWT Generado:").pack(pady=5)
        
        self.txt_token = ctk.CTkTextbox(self.dashboard_frame, height=100)
        self.txt_token.pack(pady=10, fill="x", padx=20)

        ctk.CTkButton(self.dashboard_frame, text="Cerrar Sesión", fg_color="#E74C3C", hover_color="#C0392B",
                      command=self.logout).pack(pady=20)

    def register(self):
        correo = self.entry_reg_email.get().strip()
        password = self.entry_reg_pass.get().strip()

        if not correo or not password:
            self.lbl_reg_msg.configure(text="Completa todos los campos", text_color="red")
            return

        # Encriptación unidireccional con bcrypt
        salt = bcrypt.gensalt()
        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), salt)

        try:
            self.cursor.execute("INSERT INTO usuarios (correo, password_hash) VALUES (?, ?)", (correo, hashed_pw))
            self.conn.commit()
            self.lbl_reg_msg.configure(text="Registro exitoso", text_color="green")
            self.entry_reg_email.delete(0, 'end')
            self.entry_reg_pass.delete(0, 'end')
        except sqlite3.IntegrityError:
            self.lbl_reg_msg.configure(text="El correo ya está registrado", text_color="red")

    def login(self):
        correo = self.entry_login_email.get().strip()
        password = self.entry_login_pass.get().strip()

        self.cursor.execute("SELECT id, password_hash FROM usuarios WHERE correo = ?", (correo,))
        usuario = self.cursor.fetchone()

        # Verificar credenciales y generar Token JWT
        if usuario and bcrypt.checkpw(password.encode('utf-8'), usuario[1]):
            token = jwt.encode({"id": usuario[0], "correo": correo}, SECRET_KEY, algorithm="HS256")
            
            self.txt_token.delete("1.0", "end")
            self.txt_token.insert("1.0", token)
            
            self.lbl_login_msg.configure(text="")
            self.show_frame(self.dashboard_frame)
        else:
            self.lbl_login_msg.configure(text="Credenciales incorrectas")

    def logout(self):
        self.txt_token.delete("1.0", "end")
        self.entry_login_pass.delete(0, 'end')
        self.show_frame(self.login_frame)

if __name__ == "__main__":
    app = AuthApp()
    app.mainloop()