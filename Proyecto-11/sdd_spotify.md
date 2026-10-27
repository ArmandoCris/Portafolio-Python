Rol: Desarrollador Full-Stack Avanzado.
Tarea: Construir un Clon de Spotify usando Flask, SQLite, Bootstrap 5 (Dark Mode) y HTML5 Audio.

Base de Datos (spotify.db):
- Tabla `usuarios`: id, username, password_hash. 
- Implementar rutas de Flask para Registro, Login y Logout usando `bcrypt` para las contraseñas y `session` para mantener la sesión activa.

Interfaz Gráfica (Frontend - templates/index.html):
- Layout estilo Spotify: 
  1. Barra lateral izquierda (Sidebar) oscura con el logo y un botón de "Cerrar Sesión".
  2. Área central para mostrar resultados en un grid de tarjetas (Cards).
  3. Barra de reproducción fija en la parte inferior de la pantalla (Player Bar) que contenga los controles de audio, la portada del track actual, título y artista.
- Motor de búsqueda: Un input en la parte superior del área central con un botón "Buscar".

Consumo de API y Reproducción (JavaScript Vanilla):
- Al buscar, hacer un `fetch` a la API pública de iTunes: `https://itunes.apple.com/search?term={query}&entity=song&limit=12`
- Renderizar los resultados dinámicamente en el área central mostrando `artworkUrl100` (portada), `trackName` y `artistName`.
- Cada tarjeta debe tener un botón "Play". Al hacer clic, JavaScript debe tomar el `previewUrl` del JSON, asignarlo al `src` de una etiqueta oculta `<audio>` en el Player Bar inferior, actualizar la imagen y texto del reproductor, y ejecutar `.play()` automáticamente.