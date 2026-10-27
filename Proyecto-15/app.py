import os
from flask import Flask, render_template, request, flash, redirect
import google.generativeai as genai
import PyPDF2

app = Flask(__name__)
app.secret_key = 'clave_secreta_resumen'
app.config['UPLOAD_FOLDER'] = 'uploads'

# Reemplaza TU_API_KEY_AQUI con tu clave real, manteniendo las comillas
genai.configure(api_key="TU_API_KEY_AQUI")

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/resumir', methods=['POST'])
def resumir():
    if 'documento' not in request.files:
        flash('No se subió ningún archivo.', 'danger')
        return redirect(request.url)
    
    file = request.files['documento']
    if file.filename == '':
        flash('Ningún archivo seleccionado.', 'danger')
        return render_template('index.html')

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)
    texto_extraido = ""

    try:
        # 1. Extracción de texto
        if file.filename.endswith('.pdf'):
            with open(filepath, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    texto_pagina = page.extract_text()
                    if texto_pagina:
                        texto_extraido += texto_pagina + "\n"
        elif file.filename.endswith('.txt'):
            with open(filepath, 'r', encoding='utf-8') as f:
                texto_extraido = f.read()
        else:
            os.remove(filepath)
            flash('Formato no soportado. Por favor sube un archivo PDF o TXT.', 'danger')
            return render_template('index.html')

        # 2. Validación de contenido vacío
        if not texto_extraido.strip():
            raise ValueError("El documento está vacío o PyPDF2 no pudo extraer texto legible (posible imagen escaneada).")

        # 3. Generación con IA
        prompt = f"""Actúa como un analista de datos experto. Resume el siguiente texto resaltando los puntos clave y las conclusiones principales. 
        Formatea tu respuesta estrictamente en HTML limpio (usando <p>, <ul>, <li> y <strong>). No incluyas etiquetas de bloque de código Markdown.
        Texto a resumir: {texto_extraido[:8000]}""" 
        
        # Uso del modelo más rápido y compatible con la capa gratuita
        model = genai.GenerativeModel('gemini-3.8-flash')
        respuesta = model.generate_content(prompt)
        resumen = respuesta.text

    except Exception as e:
        # Depuración en la terminal de VS Code
        print(f"\n--- ERROR REAL DE LA API --- \n{e}\n----------------------------\n")
        
        resumen = f"""
        <div class="alert alert-danger">
            <h5 class="alert-heading">Error de procesamiento</h5>
            <p>No se pudo generar el resumen con la IA. Revisa la terminal de VS Code para ver el motivo exacto del fallo.</p>
        </div>
        """
        flash('Fallo al conectar con la IA o extraer el texto. Revisa la terminal.', 'danger')
    
    finally:
        # Limpieza del servidor
        if os.path.exists(filepath):
            os.remove(filepath)
            
    return render_template('index.html', resumen=resumen, filename=file.filename)

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)