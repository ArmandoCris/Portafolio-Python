from flask import Flask, render_template, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'netflix_secret_key'

def init_db():
    conn = sqlite3.connect('netflix.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS usuarios (id INTEGER PRIMARY KEY, email TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS perfiles (id INTEGER PRIMARY KEY, user_id INTEGER, nombre TEXT, avatar TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS peliculas (id INTEGER PRIMARY KEY, titulo TEXT, categoria TEXT, img TEXT)')

    c.execute('SELECT COUNT(*) FROM peliculas')
    if c.fetchone()[0] == 0:
        c.execute("INSERT INTO usuarios (email) VALUES ('admin@netflix.com')")
        c.execute("INSERT INTO perfiles (user_id, nombre, avatar) VALUES (1, 'Luis', 'https://upload.wikimedia.org/wikipedia/commons/0/0b/Netflix-avatar.png')")
        
        peliculas = [
            ('Forrest Gump', 'Clásicos y Premiadas', 'https://via.placeholder.com/250x140/333/fff?text=Forrest+Gump'),
            ('Breaking Bad', 'Tendencias', 'https://via.placeholder.com/250x140/222/fff?text=Breaking+Bad'),
            ('Vikings', 'Acción y Épica', 'https://via.placeholder.com/250x140/444/fff?text=Vikings'),
            ('Heroes', 'Ciencia Ficción', 'https://via.placeholder.com/250x140/555/fff?text=Heroes')
        ]
        c.executemany("INSERT INTO peliculas (titulo, categoria, img) VALUES (?, ?, ?)", peliculas)
    
    conn.commit()
    conn.close()

@app.route('/')
def index():
    session['user_id'] = 1 
    conn = sqlite3.connect('netflix.db')
    perfiles = conn.execute('SELECT id, nombre, avatar FROM perfiles WHERE user_id = ?', (session['user_id'],)).fetchall()
    conn.close()
    return render_template('perfiles.html', perfiles=perfiles)

@app.route('/browse/<int:perfil_id>')
def browse(perfil_id):
    conn = sqlite3.connect('netflix.db')
    perfil = conn.execute('SELECT nombre FROM perfiles WHERE id = ?', (perfil_id,)).fetchone()
    rows = conn.execute('SELECT titulo, categoria, img FROM peliculas').fetchall()
    conn.close()

    catalogo = {}
    for titulo, categoria, img in rows:
        if categoria not in catalogo:
            catalogo[categoria] = []
        catalogo[categoria].append({'titulo': titulo, 'img': img})

    return render_template('browse.html', perfil=perfil[0], catalogo=catalogo)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)