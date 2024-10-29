from flask import Flask, render_template, request, jsonify
from rag import crear_rag_system, hacer_pregunta
import config

app = Flask(__name__)

# Sistemas RAG para diferentes modelos
rag_systems = {
    'claude': None,
    'gpt4': None,
    'mistral': None
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/preguntar', methods=['POST'])
def preguntar():
    if not request.is_json:
        return jsonify({'error': 'Se esperaba JSON'}), 400

    data = request.json
    pregunta = data.get('pregunta')
    modelo = data.get('modelo', 'claude')

    print(f"Modelo seleccionado: {modelo}")  # Debug

    if not pregunta:
        return jsonify({'error': 'No se recibió ninguna pregunta'}), 400

    if modelo not in ['claude', 'gpt4', 'mistral']:
        return jsonify({'error': 'Modelo no válido'}), 400

    # Inicializar el sistema RAG si no existe para el modelo seleccionado
    if modelo not in rag_systems or rag_systems[modelo] is None:
        try:
            print(f"Inicializando sistema RAG para {modelo}")  # Debug
            rag_systems[modelo] = crear_rag_system(modelo)
        except Exception as e:
            print(f"Error inicializando {modelo}: {str(e)}")  # Debug
            return jsonify({'error': f'Error inicializando el modelo: {str(e)}'}), 500

    try:
        # Llamamos a hacer_pregunta con el sistema RAG correcto
        respuesta = hacer_pregunta(rag_systems[modelo], pregunta)
        return jsonify(respuesta)
    except Exception as e:
        print(f"Error en pregunta con {modelo}: {str(e)}")  # Debug
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
