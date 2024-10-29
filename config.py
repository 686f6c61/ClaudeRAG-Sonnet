from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

# Obtener API key desde variables de entorno
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
MISTRAL_API_KEY = os.getenv('MISTRAL_API_KEY')
FLASK_SECRET_KEY = os.getenv('FLASK_SECRET_KEY')
if not ANTHROPIC_API_KEY:
    raise ValueError("No se encontró la clave API de Anthropic en las variables de entorno")

# Debug para verificar que la clave se carga (quitar en producción)
print("Primeros 8 caracteres de ANTHROPIC_API_KEY:", ANTHROPIC_API_KEY[:8] if ANTHROPIC_API_KEY else "No encontrada")

DOCUMENTOS_DIR = "documentos"