from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'clave_secreta_reservas'

def init_db():
    conn = sqlite3.connect('reservas.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS citas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente TEXT,
            fecha_inicio TEXT,
            fecha_fin TEXT,
            color TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/eventos')
def api_eventos():
    conn = sqlite3.connect('reservas.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, cliente, fecha_inicio, fecha_fin, color FROM citas")
    citas = cursor.fetchall()
    conn.close()

    # Formateamos los datos exactamente como FullCalendar los exige
    eventos = []
    for cita in citas:
        eventos.append({
            'id': cita[0],
            'title': cita[1],
            'start': cita[2],
            'end': cita[3],
            'backgroundColor': cita[4],
            'borderColor': cita[4]
        })
    return jsonify(eventos)

@app.route('/reservar', methods=['POST'])
def reservar():
    cliente = request.form.get('cliente')
    fecha_inicio = request.form.get('fecha_inicio')
    fecha_fin = request.form.get('fecha_fin')
    color = request.form.get('color', '#0d6efd') # Azul por defecto

    if cliente and fecha_inicio and fecha_fin:
        conn = sqlite3.connect('reservas.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO citas (cliente, fecha_inicio, fecha_fin, color) VALUES (?, ?, ?, ?)",
                       (cliente, fecha_inicio, fecha_fin, color))
        conn.commit()
        conn.close()
        flash('Reserva confirmada con éxito.', 'success')
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)