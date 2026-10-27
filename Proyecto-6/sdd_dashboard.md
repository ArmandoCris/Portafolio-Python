Rol: Desarrollador experto en Python y análisis de datos.
Tarea: Crear un "Dashboard de Finanzas" integrando CustomTkinter, SQLite y Matplotlib.
Base de Datos (finanzas.db):

Crear tabla movimientos con: id, mes (TEXT), tipo (TEXT), categoria (TEXT), monto (REAL).

Crear un método inyectar_datos_prueba que inserte 10 registros ficticios (ingresos y gastos de diferentes categorías) si la tabla está vacía, para garantizar que haya datos para graficar.
Interfaz Gráfica (800x600, Tema Oscuro):

Panel Superior (KPIs): Tres CTkLabel grandes mostrando la sumatoria real de: Total Ingresos, Total Gastos y Saldo Neto.

Panel Inferior (Lienzo del Gráfico): Un marco amplio.
Lógica del Gráfico (Matplotlib):

Consulta SQLite para sumar los gastos agrupados por categoria.

Crea una figura de Matplotlib (gráfico de barras o pastel) con fondo oscuro para que coincida con el tema de CustomTkinter.

Usa FigureCanvasTkAgg (de matplotlib.backends.backend_tkagg) para incrustar el gráfico dentro del Panel Inferior.