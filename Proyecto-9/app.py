from flask import Flask, jsonify, render_template
import sqlite3
from datetime import datetime

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('cms.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS articulos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT,
            contenido TEXT,
            fecha_publicacion TEXT
        )
    ''')
    
    cursor.execute("SELECT COUNT(*) FROM articulos")
    if cursor.fetchone()[0] == 0:
        fecha_actual = datetime.now().strftime("%Y-%m-%d")
        articulos_iniciales = [
            ('Introducción a Vibe Coding', 'El Vibe Coding combina la intuición humana con la generación de código por IA para iterar rápidamente.', fecha_actual),
            ('Por qué SQLite es increíble', 'Las bases de datos locales ofrecen una velocidad inigualable y no dependen de la nube para funcionar.', fecha_actual),
            ('Arquitecturas Headless', 'Separar el frontend del backend permite que múltiples plataformas (Web, Móvil, Escritorio) consuman la misma API.', fecha_actual)
        ]
        cursor.executemany("INSERT INTO articulos (titulo, contenido, fecha_publicacion) VALUES (?, ?, ?)", articulos_iniciales)
        conn.commit()
    conn.close()

# --- RUTAS DEL HEADLESS CMS (Solo Datos) ---
@app.route('/api/articulos', methods=['GET'])
def obtener_articulos():
    conn = sqlite3.connect('cms.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, titulo, contenido, fecha_publicacion FROM articulos ORDER BY id DESC")
    columnas = [desc[0] for desc in cursor.description]
    
    # Convertir las tuplas de SQLite a una lista de diccionarios JSON
    articulos = [dict(zip(columnas, fila)) for fila in cursor.fetchall()]
    conn.close()
    
    return jsonify(articulos)

# --- RUTA DEL FRONTEND ---
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)