from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import bcrypt

app = Flask(__name__)
app.secret_key = 'clave_secreta_spotify'

def init_db():
    conn = sqlite3.connect('spotify.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password_hash BLOB
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('index.html', username=session['username'])

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        salt = bcrypt.gensalt()
        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), salt)
        
        try:
            conn = sqlite3.connect('spotify.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO usuarios (username, password_hash) VALUES (?, ?)", (username, hashed_pw))
            conn.commit()
            conn.close()
            flash('Registro exitoso. Inicia sesión.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('El usuario ya existe.', 'danger')
            
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect('spotify.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, password_hash FROM usuarios WHERE username = ?", (username,))
        usuario = cursor.fetchone()
        conn.close()
        
        if usuario and bcrypt.checkpw(password.encode('utf-8'), usuario[2]):
            session['user_id'] = usuario[0]
            session['username'] = usuario[1]
            return redirect(url_for('index'))
        else:
            flash('Credenciales incorrectas.', 'danger')
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)