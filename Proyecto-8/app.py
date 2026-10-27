from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'clave_secreta_ecommerce'

def init_db():
    conn = sqlite3.connect('tienda.db')
    cursor = conn.cursor()
    
    # Reiniciamos la tabla para agregar la columna de stock sin errores
    cursor.execute("DROP TABLE IF EXISTS productos")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            precio REAL,
            imagen TEXT,
            stock INTEGER
        )
    ''')
    
    # Inyectamos los productos, esta vez con una cantidad de stock inicial
    productos_iniciales = [
        ('Laptop Gamer', 1200.00, '💻', 5),
        ('Auriculares Inalámbricos', 150.00, '🎧', 10),
        ('Teclado Mecánico', 85.00, '⌨️', 8),
        ('Monitor 4K', 300.00, '🖥️', 3),
        ('Ratón Ergonómico', 45.00, '🖱️', 15),
        ('Cámara Web HD', 60.00, '📷', 7)
    ]
    cursor.executemany("INSERT INTO productos (nombre, precio, imagen, stock) VALUES (?, ?, ?, ?)", productos_iniciales)
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('tienda.db')
    cursor = conn.cursor()
    # Ahora consultamos también el stock (índice 4)
    cursor.execute("SELECT id, nombre, precio, imagen, stock FROM productos")
    productos = cursor.fetchall()
    conn.close()
    
    if 'carrito' not in session:
        session['carrito'] = []
        
    return render_template('index.html', productos=productos, cantidad_carrito=len(session['carrito']))

@app.route('/agregar/<int:id>')
def agregar(id):
    if 'carrito' not in session:
        session['carrito'] = []
    
    carrito = session['carrito']
    cantidad_en_carrito = carrito.count(id)
    
    # Consultar si el stock es suficiente para agregar uno más
    conn = sqlite3.connect('tienda.db')
    cursor = conn.cursor()
    cursor.execute("SELECT stock FROM productos WHERE id = ?", (id,))
    resultado = cursor.fetchone()
    conn.close()

    if resultado and resultado[0] > cantidad_en_carrito:
        carrito.append(id)
        session['carrito'] = carrito
        flash('Producto agregado al carrito', 'success')
    else:
        flash('No hay suficiente stock disponible para este producto.', 'danger')

    return redirect(url_for('index'))

@app.route('/carrito')
def ver_carrito():
    if 'carrito' not in session or not session['carrito']:
        return render_template('carrito.html', productos_carrito=[], total=0.0, cantidad_carrito=0)
        
    conn = sqlite3.connect('tienda.db')
    cursor = conn.cursor()
    
    ids = session['carrito']
    placeholders = ','.join('?' for _ in set(ids))
    cursor.execute(f"SELECT id, nombre, precio, imagen FROM productos WHERE id IN ({placeholders})", list(set(ids)))
    productos_db = {row[0]: row for row in cursor.fetchall()}
    conn.close()
    
    productos_carrito = []
    total = 0.0
    for pid in ids:
        if pid in productos_db:
            producto = productos_db[pid]
            productos_carrito.append(producto)
            total += producto[2]
            
    return render_template('carrito.html', productos_carrito=productos_carrito, total=total, cantidad_carrito=len(ids))

@app.route('/pagar')
def pagar():
    if 'carrito' not in session or not session['carrito']:
        return redirect(url_for('index'))

    conn = sqlite3.connect('tienda.db')
    cursor = conn.cursor()
    
    # Descontamos 1 unidad del stock por cada vez que el ID aparezca en el carrito
    for pid in session['carrito']:
        cursor.execute("UPDATE productos SET stock = stock - 1 WHERE id = ? AND stock > 0", (pid,))
        
    conn.commit()
    conn.close()

    session.pop('carrito', None)
    flash('¡Compra realizada con éxito! El inventario ha sido actualizado.', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)