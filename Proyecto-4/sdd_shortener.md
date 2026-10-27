Rol: Desarrollador experto en Python.
Tarea: Crear una aplicación "URL Shortener" local usando CustomTkinter, SQLite y pyperclip.
Base de Datos (urls.db):

Crear tabla enlaces con: id (INTEGER PRIMARY KEY), url_original (TEXT), codigo_corto (TEXT), y clics (INTEGER DEFAULT 0).
Lógica Principal:

Importar random y string para generar códigos alfanuméricos únicos de 6 caracteres (ej. "xK9mP2").

Método acortar_url: Lee el entry de la URL original, genera el código, hace el INSERT en SQLite y recarga el historial en pantalla.

Método copiar_y_usar: Recibe el ID del enlace. Hace un UPDATE en la base de datos sumando +1 a clics. Usa pyperclip.copy() para copiar un dominio simulado más el código (ej. "http://mi.url/xK9mP2") al portapapeles. Recarga el historial.
Interfaz Gráfica (550x600, tema oscuro):

Parte superior: Un CTkEntry ancho para la URL original y un CTkButton "Acortar URL".

Parte inferior: Un CTkScrollableFrame para el historial.

Cada fila del historial debe ser un CTkFrame que contenga: la URL original (truncada si es muy larga), el código corto, la cantidad de "clics", y un CTkButton pequeño que diga "Copiar" asociado al método copiar_y_usar.