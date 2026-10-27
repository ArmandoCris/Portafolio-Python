Rol: Desarrollador Backend Python.
Tarea: Crear una sala de "Chat en tiempo real" usando Flask, Flask-SocketIO y Bootstrap 5.

Backend (app.py):
- Configurar Flask y SocketIO (`socketio = SocketIO(app)`).
- Ruta `/`: Renderiza `index.html`.
- Evento de SocketIO `on('message')`: Recibe un diccionario con 'username' y 'text', y lo retransmite a todos los clientes conectados usando `send(msg, broadcast=True)`.

Frontend (templates/index.html):
- Interfaz oscura con Bootstrap.
- Un contenedor con `overflow-y: scroll` para el historial del chat.
- Dos inputs: Nombre de usuario y Mensaje, más un botón "Enviar".
- Importar el cliente de Socket.IO vía CDN (`socket.io.js`).
- Lógica JS: Conectar con `const socket = io()`. Al hacer clic en "Enviar" o presionar Enter, emitir el mensaje. Al recibir un evento 'message', inyectar el texto en el historial y hacer auto-scroll hacia abajo.