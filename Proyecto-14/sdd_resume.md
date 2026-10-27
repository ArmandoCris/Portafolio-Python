Rol: Ingeniero de IA y Desarrollador Flask.
Tarea: Construir un "AI Resume Builder" que tome datos básicos y genere un CV profesional redactado mediante IA.

Backend (app.py):
- Configurar `google.generativeai` para interactuar con el modelo `gemini-pro`.
- Ruta `/`: Renderiza el formulario de entrada.
- Ruta `/generar` (POST): Recibe Nombre, Títulos, Habilidades y Experiencia.
- Construir un "Prompt" estricto que instruya a la IA a actuar como reclutador y devolver un resumen en formato HTML (<h3>, <p>, <ul>).
- Implementar un bloque `try-except`: Si no hay una API Key válida configurada, devolver un CV de respaldo pre-generado para evitar que la aplicación falle durante la demostración.

Frontend (templates/index.html):
- Diseño profesional a dos columnas usando Bootstrap 5.
- Columna Izquierda: Formulario de ingreso de datos.
- Columna Derecha: Panel de previsualización donde se inyectará dinámicamente la respuesta HTML de la IA usando la etiqueta `|safe` de Jinja2.