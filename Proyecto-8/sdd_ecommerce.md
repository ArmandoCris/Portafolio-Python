Rol: Desarrollador Full-Stack Python.
Tarea: Crear un "E-Commerce Básico" usando Flask, SQLite y Bootstrap 5 (vía CDN).

Base de Datos (tienda.db):
- Tabla "productos": id (INTEGER PRIMARY KEY), nombre (TEXT), precio (REAL), imagen (TEXT - usa emojis o URLs de prueba).
- Inyectar 6 productos iniciales ficticios (ej. tecnología o ropa) si la tabla está vacía al arrancar.

Backend (app.py):
- Configurar la aplicación Flask con una `secret_key` para habilitar el uso de sesiones web (aquí vivirá el carrito temporal).
- Ruta `/`: Consulta todos los productos en SQLite y renderiza el catálogo.
- Ruta `/agregar/<int:id>`: Añade el ID del producto a la sesión del carrito y redirige al inicio.
- Ruta `/carrito`: Cruza los IDs de la sesión con la base de datos, calcula el subtotal y renderiza la vista de pago.
- Ruta `/pagar`: Vacía el carrito de la sesión, simula una compra exitosa mediante un mensaje (flash) y redirige al catálogo.

Frontend (Carpeta templates/):
- Crear `layout.html`: Plantilla base con un Navbar oscuro de Bootstrap. Debe incluir un enlace al carrito mostrando la cantidad actual de ítems almacenados en la sesión.
- Crear `index.html` (hereda de layout): Usa un sistema de "Cards" en Grid para mostrar el catálogo. Cada tarjeta tiene un botón "Agregar al carrito".
- Crear `carrito.html` (hereda de layout): Muestra una tabla limpia con los productos seleccionados, el precio total y un botón verde de "Finalizar Compra".