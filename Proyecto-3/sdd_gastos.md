Rol: Desarrollador experto en Python y CustomTkinter.
Tarea: Crear una aplicación de "Expense Tracker" con interfaz gráfica y persistencia en SQLite.
Requerimientos de Base de Datos:

Crear/conectar a gastos.db.

Crear tabla transacciones con columnas: id (INTEGER PRIMARY KEY), tipo (TEXT, será "Ingreso" o "Gasto"), monto (REAL), y descripcion (TEXT).
Requerimientos de UI (Ventana 500x700, tema oscuro):

Estadísticas (Top): Un marco con tres CTkLabel destacados para mostrar: "Total Ingresos: $0", "Total Gastos: $0" y "Balance: $0".

Formulario (Centro):

Un CTkOptionMenu para seleccionar el tipo ("Ingreso", "Gasto").

Un CTkEntry para ingresar el Monto.

Un CTkEntry para ingresar la Descripción.

Un CTkButton "Agregar Transacción" que inserte el registro en SQLite.

Historial (Fondo): Un CTkScrollableFrame que muestre todas las transacciones guardadas. Cada fila debe mostrar el tipo, monto y descripción.
Lógica Principal:

Un método calcular_estadisticas que sume todos los montos de "Ingreso", sume todos los montos de "Gasto", calcule la diferencia (Balance) y actualice los labels de estadísticas.

Al presionar "Agregar", se guarda en DB, se actualiza el historial en pantalla, se limpian los campos y se recalculan las estadísticas inmediatamente.

Al abrir la app, se deben cargar los datos existentes y mostrar las estadísticas reales.