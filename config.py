import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Obtener API key desde variables de entorno
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
if not ANTHROPIC_API_KEY:
    raise ValueError("No se encontró ANTHROPIC_API_KEY en las variables de entorno")

DOCUMENTOS_DIR = "documentos"