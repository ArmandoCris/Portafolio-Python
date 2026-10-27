Rol: Desarrollador experto en Python y ciberseguridad.
Tarea: Crear una aplicación de escritorio con sistema de autenticación usando CustomTkinter, SQLite, bcrypt y PyJWT.
Base de Datos (usuarios.db):

Crea la tabla usuarios con: id (INTEGER PRIMARY KEY), correo (TEXT UNIQUE), y password_hash (BLOB).
Lógica de Seguridad:

Registro: Recibe correo y contraseña. Usa bcrypt.gensalt() y bcrypt.hashpw() para encriptar la contraseña (convertida a bytes) y guárdala en SQLite.

Login: Busca el correo en la base de datos. Usa bcrypt.checkpw() para verificar la contraseña ingresada contra el hash de la base de datos. Si es correcta, genera un token con jwt.encode({"id": usuario_id}, "secreto", algorithm="HS256").
Interfaz Gráfica (400x500, Tema Oscuro):

Diseña una clase base que gestione múltiples "Frames" (pantallas) usando .pack_forget() para ocultarlas y .pack() para mostrarlas.

Frame de Login: Entradas para correo y contraseña (oculta con show="*"). Botón "Iniciar Sesión", botón "Crear Cuenta" (cambia a vista Registro) y botón "Recuperar Contraseña".

Frame de Registro: Entradas para correo, contraseña y confirmar contraseña. Botones "Registrar" y "Volver al Login".

Frame Dashboard (Área Privada): Solo accesible tras un login exitoso. Debe mostrar un mensaje de bienvenida, un CTkTextbox que imprima el Token JWT generado (para verificar visualmente que funciona), y un botón "Cerrar Sesión" que borre el token en memoria y vuelva al Login.