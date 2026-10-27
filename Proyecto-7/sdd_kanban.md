Rol: Desarrollador experto en Python.
Tarea: Crear un Administrador de Tareas Kanban local con CustomTkinter y SQLite.

Base de Datos (kanban.db):
- Tabla "tareas": id (INTEGER PRIMARY KEY), titulo (TEXT), descripcion (TEXT), estado (TEXT).
- Estados permitidos: "Pendiente", "En Progreso", "Completada".

Lógica de Transición:
- Usa botones direccionales (◀ y ▶) en cada tarjeta para mover tareas entre columnas de forma segura, evitando conflictos de drag & drop de CustomTkinter.
- Botón para eliminar tareas (🗑).

Interfaz Gráfica (1000x600, Tema Oscuro):
- Panel Superior: Entradas para Título/Descripción y botón "Añadir Tarea".
- Panel Inferior: Tres CTkScrollableFrame distribuidos en grid.
- Columna 1: "📌 Pendiente" (Gris/Azul oscuro).
- Columna 2: "⏳ En Progreso" (Naranja).
- Columna 3: "✅ Completada" (Verde).
- Cada tarjeta muestra título, descripción y los botones de acción correspondientes.