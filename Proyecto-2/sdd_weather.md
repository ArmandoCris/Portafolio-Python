Rol: Desarrollador experto en Python y CustomTkinter.
Tarea: Crear la interfaz base para una aplicación del clima (Weather App).
Requerimientos de UI:

Ventana principal de 400x500 píxeles, tema oscuro.

Un campo de entrada (CTkEntry) en la parte superior para escribir el nombre de una ciudad.

Un botón (CTkButton) que diga "Buscar Clima".

Un CTkLabel con fuente grande (ej. tamaño 50) y centrado para mostrar la temperatura (texto por defecto: "--°C").

Un CTkLabel secundario debajo para mostrar la descripción del clima (texto por defecto: "Esperando ciudad...").
Lógica base:

Crea un método buscar_clima que se ejecute al presionar el botón.

Por ahora, este método solo debe leer el texto ingresado e imprimir en consola "Buscando clima para: [Ciudad]". Todavía no usaremos la librería requests.