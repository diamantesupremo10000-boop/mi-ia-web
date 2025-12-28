import os
from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv

# Cargar variables de entorno (para desarrollo local)
load_dotenv()

app = Flask(__name__)

# Configuración del cliente OpenAI
# NOTA: En Render, la API Key se configurará en el dashboard, no en un archivo.
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/generate', methods=['POST'])
def generate():
    try:
        data = request.json
        user_prompt = data.get('prompt', '')

        if not user_prompt:
            return jsonify({'error': 'Por favor escribe algo.'}), 400

        # Llamada a la IA
        response = client.chat.completions.create(
            model="gpt-4o-mini", # O "gpt-3.5-turbo"
            messages=[
                {"role": "system", "content": "Eres un asistente útil y conciso."},
                {"role": "user", "content": user_prompt}
            ]
        )
        
        ai_reply = response.choices[0].message.content
        return jsonify({'result': ai_reply})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
