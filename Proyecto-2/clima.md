Rol: Desarrollador experto en Python.
Tarea: Actualizar el método buscar_clima de la Weather App para consumir una API real y actualizar los textos de la interfaz gráfica.
Requerimientos Técnicos:

Importar la librería requests al inicio del archivo.

Dentro del método buscar_clima, usar requests.get() para hacer una petición a la API: [https://wttr.in/](https://wttr.in/){ciudad}?format=j1 (reemplazando {ciudad} por el texto ingresado).

Procesar la respuesta JSON para extraer la temperatura actual (ubicada en current_condition[0]['temp_C']) y la descripción del clima (current_condition[0]['lang_es'][0]['value'] o en su defecto current_condition[0]['weatherDesc'][0]['value']).

Actualizar self.temperature_label y self.description_label utilizando el método .configure(text=...) con los nuevos datos.

Manejo de Errores: Envolver la petición en un bloque try/except. Si hay un error de red o la ciudad no existe, actualizar el description_label con el texto "Error: Ciudad no encontrada" y la temperatura a "--°C".