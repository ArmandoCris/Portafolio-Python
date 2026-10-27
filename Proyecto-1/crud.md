Rol: Desarrollador experto en Python y CustomTkinter.
Tarea: Actualizar el código de la To-Do App para incluir persistencia de datos usando la librería nativa sqlite3 y completar las operaciones CRUD.
Requerimientos de Base de Datos:

Crea un método que se ejecute al iniciar la app para conectarse a un archivo todo.db (si no existe, debe crearlo).

Crea una tabla llamada tareas con las columnas: id (INTEGER PRIMARY KEY AUTOINCREMENT), descripcion (TEXT), y completada (INTEGER, 0 o 1).
Requerimientos de UI y Lógica CRUD:

Read: Al iniciar la app, debe consultar la base de datos y renderizar todas las tareas guardadas.

Create: Al agregar una tarea, debe hacer el INSERT en la base de datos y luego mostrarla en la interfaz.

Update & Delete (Nuevos Widgets): Modifica el método de renderizado. En lugar de un simple CTkLabel, cada tarea dentro del task_frame debe ser un CTkFrame (un contenedor horizontal) que agrupe:

Un CTkCheckBox con el texto de la tarea. Si se marca/desmarca, debe hacer un UPDATE en la base de datos cambiando el estado de completada.

Un CTkButton pequeño (color rojo) con el texto "X". Al presionarlo, debe hacer un DELETE en la base de datos y destruir ese widget específico de la interfaz.