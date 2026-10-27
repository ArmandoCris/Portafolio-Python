Rol: Ingeniero Backend IA.
Tarea: Crear un "AI Document Summarizer" usando Flask, PyPDF2 y Bootstrap 5.

Base de Datos: 
- No se requiere base de datos persistente. Los archivos se guardan temporalmente en la carpeta `uploads/`.

Backend (app.py):
- Configurar `app.config['UPLOAD_FOLDER']` para alojar los archivos.
- Ruta `/` (GET): Renderiza el formulario de carga.
- Ruta `/resumir` (POST): 
  1. Recibe el archivo mediante `request.files`.
  2. Lo guarda localmente.
  3. Si es .txt, lee el texto plano. Si es .pdf, usa `PyPDF2.PdfReader` para extraer el texto de todas las páginas.
  4. Envía el texto a la IA con un prompt solicitando un resumen en formato HTML.
  5. Elimina el archivo físico de `uploads/` por seguridad.
  6. En caso de no tener API Key, devuelve un texto de simulación estructurado en HTML.

Frontend (templates/index.html):
- Formulario de subida con el atributo `enctype="multipart/form-data"` obligatorio para transmitir archivos.
- Un panel inferior para inyectar el HTML del resumen usando el filtro `|safe`.