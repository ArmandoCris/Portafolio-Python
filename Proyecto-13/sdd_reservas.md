Rol: Desarrollador Full-Stack Avanzado.
Tarea: Crear un Sistema de Reservas usando Flask, SQLite, Bootstrap 5 y FullCalendar.js.

Base de Datos (reservas.db):
- Tabla `citas`: id, cliente, fecha_inicio, fecha_fin, color_estado.

Backend (app.py):
- `/`: Renderiza la vista principal con el calendario.
- `/api/eventos`: Devuelve todas las citas en formato JSON adaptado a las propiedades estrictas de FullCalendar (title, start, end, backgroundColor).
- `/reservar`: Recibe una petición POST desde un modal de Bootstrap para insertar una nueva cita y redirige al inicio.

Frontend (templates/index.html):
- Layout limpio con Bootstrap.
- Contenedor div con id "calendar" para inicializar FullCalendar.js vía CDN.
- Al hacer clic en un día del calendario, abrir un Modal de Bootstrap para pedir el nombre del cliente y enviar el formulario a `/reservar`.