import customtkinter as ctk
import requests  # Importar la librería requests

# Configuración de la ventana principal
class WeatherApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuración de la ventana
        self.title("Weather App")
        self.geometry("400x500")
        ctk.set_appearance_mode("dark")  # Tema oscuro

        # Campo de entrada para la ciudad
        self.city_entry = ctk.CTkEntry(self, placeholder_text="Ingrese el nombre de la ciudad")
        self.city_entry.pack(pady=20, padx=20)

        # Botón para buscar el clima
        self.search_button = ctk.CTkButton(self, text="Buscar Clima", command=self.buscar_clima)
        self.search_button.pack(pady=10)

        # Label para mostrar la temperatura
        self.temperature_label = ctk.CTkLabel(self, text="--°C", font=("Arial", 50), justify="center")
        self.temperature_label.pack(pady=20)

        # Label para mostrar la descripción del clima
        self.description_label = ctk.CTkLabel(self, text="Esperando ciudad...", font=("Arial", 16))
        self.description_label.pack(pady=10)

    # Método para buscar el clima
    def buscar_clima(self):
        ciudad = self.city_entry.get()
        if not ciudad.strip():
            self.description_label.configure(text="Error: Ingrese una ciudad válida")
            self.temperature_label.configure(text="--°C")
            return

        try:
            # Hacer la petición a la API
            url = f"https://wttr.in/{ciudad}?format=j1"
            response = requests.get(url)
            response.raise_for_status()  # Verificar si hubo errores en la petición

            # Procesar la respuesta JSON
            data = response.json()
            temperatura = data['current_condition'][0]['temp_C']
            descripcion = data['current_condition'][0].get('lang_es', [{}])[0].get('value', 
                          data['current_condition'][0]['weatherDesc'][0]['value'])

            # Actualizar los labels con los datos obtenidos
            self.temperature_label.configure(text=f"{temperatura}°C")
            self.description_label.configure(text=descripcion)

        except Exception as e:
            # Manejo de errores
            self.description_label.configure(text="Error: Ciudad no encontrada")
            self.temperature_label.configure(text="--°C")

# Ejecutar la aplicación
if __name__ == "__main__":
    app = WeatherApp()
    app.mainloop()