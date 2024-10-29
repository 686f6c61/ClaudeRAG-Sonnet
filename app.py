from flask import Flask, render_template, request, jsonify, url_for
from config import ANTHROPIC_API_KEY, DOCUMENTOS_DIR
from rag import crear_rag, hacer_pregunta
import os

app = Flask(__name__, static_folder='static')
historial_chat = []

# Inicializar RAG al inicio
def inicializar_rag():
    pdfs = [f for f in os.listdir(DOCUMENTOS_DIR) if f.endswith('.pdf')]
    if not pdfs:
        return None, "No se encontraron PDFs en el directorio documentos"
    try:
        return crear_rag(DOCUMENTOS_DIR, ANTHROPIC_API_KEY, pdfs), None
    except Exception as e:
        return None, str(e)

rag_system, error = inicializar_rag()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/preguntar', methods=['POST'])
def preguntar():
    if not request.is_json:
        return jsonify({'error': 'Se esperaba JSON'}), 400

    pregunta = request.json.get('pregunta')
    if not pregunta:
        return jsonify({'error': 'No se recibió ninguna pregunta'}), 400

    try:
        respuesta = hacer_pregunta(rag_system, pregunta, historial_chat)
        historial_chat.append((pregunta, respuesta["respuesta"]))
        
        return jsonify({
            'respuesta': respuesta["respuesta"],
            'fuentes': respuesta.get("fuentes", "")
        })
    except Exception as e:
        print(f"Error procesando pregunta: {str(e)}")  # Para debugging
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
