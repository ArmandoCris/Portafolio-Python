Rol: Arquitecto de Software Python.
Tarea: Crear un Blog con arquitectura Headless usando Flask, SQLite y JavaScript Vanilla.

Base de Datos (cms.db):
- Tabla "articulos": id, titulo, contenido, fecha_publicacion.
- Inyectar 3 artículos de prueba sobre tecnología o programación al inicializar.

Backend (API Headless - app.py):
- Ruta `/api/articulos`: Devuelve exclusivamente un JSON con todos los artículos ordenados por fecha. No renderiza HTML. Esta es la esencia del "Headless CMS".
- Ruta `/`: Renderiza el archivo estático `index.html`.

Frontend (templates/index.html):
- Plantilla HTML pura con Bootstrap 5 (CDN).
- Usa JavaScript (`fetch('/api/articulos')`) para consumir el JSON del backend de forma asíncrona.
- Construye el DOM dinámicamente inyectando los artículos en tarjetas de Bootstrap.