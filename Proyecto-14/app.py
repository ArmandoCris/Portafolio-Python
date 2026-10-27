from flask import Flask, render_template, request, flash
import google.generativeai as genai

app = Flask(__name__)
app.secret_key = 'clave_secreta_cv'

# Para usar la IA real, consigue una API Key gratuita en Google AI Studio 
# y descomenta la siguiente línea, reemplazando el texto:
# genai.configure(api_key="TU_API_KEY_AQUI") 

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/generar', methods=['POST'])
def generar():
    nombre = request.form.get('nombre')
    titulos = request.form.get('titulos')
    habilidades = request.form.get('habilidades')
    experiencia = request.form.get('experiencia')
    
    prompt = f"""
    Actúa como un reclutador experto y redactor de currículums de alto nivel.
    Escribe un perfil profesional atractivo y 3 logros destacados para el siguiente candidato:
    Nombre: {nombre}
    Cargo: {titulos}
    Habilidades clave: {habilidades}
    Experiencia general: {experiencia}
    
    El formato de tu respuesta debe ser estrictamente HTML limpio (usando solo <h3>, <p>, y <ul><li>) listo para inyectarse en una web. No incluyas Markdown ni etiquetas ```html.
    """
    
    try:
        # Intenta generar el contenido con la IA real
        model = genai.GenerativeModel('gemini-pro')
        respuesta = model.generate_content(prompt)
        cv_generado = respuesta.text
    except Exception as e:
        # Fallback de simulación inteligente para que la app no colapse en desarrollo
        cv_generado = f"""
        <h3 class="text-primary border-bottom pb-2">Perfil Profesional</h3>
        <p class="lead">Profesional altamente capacitado combinando experiencia técnica avanzada como <strong>{titulos}</strong> con dominio sólido en herramientas tecnológicas ({habilidades}). Demuestra un historial comprobado de optimización de procesos operativos, análisis crítico de datos y entrega de soluciones en entornos de alta exigencia.</p>
        <h3 class="text-primary border-bottom pb-2 mt-4">Logros y Capacidades Destacadas</h3>
        <ul class="fs-5">
            <li class="mb-2">Aportó {experiencia} garantizando la precisión técnica, la integridad estructural y el control estricto de parámetros críticos.</li>
            <li class="mb-2">Diseñó e integró arquitecturas de software modernas con flujos de trabajo operativos para automatizar la captura y gestión de datos.</li>
            <li class="mb-2">Lideró la evaluación y diagnóstico preciso en tiempo real para apoyar la toma de decisiones gerenciales.</li>
        </ul>
        """
        flash('Nota: Estás viendo un renderizado de prueba. Configura tu API Key de Gemini para activar la generación por IA real.', 'warning')
        
    return render_template('index.html', cv_generado=cv_generado, nombre=nombre, titulos=titulos)

if __name__ == '__main__':
    app.run(debug=True)