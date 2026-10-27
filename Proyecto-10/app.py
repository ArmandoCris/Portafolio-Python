from flask import Flask, render_template
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secreto_chat_123'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

# Escucha los mensajes entrantes a través del WebSocket
@socketio.on('message')
def handle_message(msg):
    # El parámetro broadcast=True envía el mensaje a todos los usuarios conectados
    send(msg, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)