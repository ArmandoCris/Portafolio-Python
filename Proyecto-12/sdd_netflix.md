Rol: Desarrollador Full-Stack Avanzado.
Tarea: Crear un Clon de Netflix con Flask, SQLite y Bootstrap 5 (Dark Mode).

Base de Datos (netflix.db):
- Tabla `usuarios`: id, email.
- Tabla `perfiles`: id, user_id (Foránea), nombre, avatar (URL).
- Tabla `peliculas`: id, titulo, categoria, img_url.

Flujo del Backend (app.py):
- `/`: Selecciona automáticamente al usuario de prueba y renderiza la pantalla de perfiles.
- `/browse/<perfil_id>`: El catálogo principal. Consulta todas las películas, las agrupa por categoría mediante un diccionario en Python y las pasa a la plantilla.

Frontend (templates/):
- `perfiles.html`: Fondo oscuro, muestra los avatares cuadrados en el centro para seleccionar quién está viendo.
- `browse.html`: Navbar fijo. Las categorías se muestran como filas horizontales usando CSS `overflow-x: scroll` ocultando la barra de desplazamiento. Efecto `:hover` con `transform: scale(1.08)` en las portadas.