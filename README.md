 # RAG MultiLLM

## Descripción
RAG MultiLLM es un sistema de Recuperación Aumentada de Generación (RAG) que integra múltiples modelos de lenguaje de última generación. Esta aplicación permite interactuar con tres de los LLMs más potentes del mercado: Claude 3 Sonnet de Anthropic, GPT-4 Turbo de OpenAI y Mistral Large de Mistral AI. El sistema está diseñado para proporcionar respuestas contextualizadas y precisas basadas en documentos PDF proporcionados por el usuario.

## Características Principales
- **Múltiples Modelos**: Integración con tres LLMs líderes:
  - Claude 3 Sonnet (Anthropic)
  - GPT-4 Turbo (OpenAI)
  - Mistral Large (Mistral AI)
- **Sistema RAG Avanzado**: Procesamiento y recuperación inteligente de información desde documentos PDF
- **Interfaz Moderna**: UI/UX intuitiva con Material Design
- **Respuestas Estructuradas**: Formato HTML enriquecido con referencias y citas
- **Procesamiento Asíncrono**: Manejo eficiente de solicitudes y respuestas

## Requisitos Previos
- Python 3.10 o superior
- pip (gestor de paquetes de Python)
- Claves API de:
  - Anthropic (Claude)
  - OpenAI (GPT-4)
  - Mistral AI

## Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/yourusername/rag-multillm.git
cd rag-multillm
```

2. Crear y activar entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## Configuración
Crear un archivo `.env` en la raíz del proyecto:
```env
ANTHROPIC_API_KEY=your_anthropic_api_key
OPENAI_API_KEY=your_openai_api_key
MISTRAL_API_KEY=your_mistral_api_key
FLASK_SECRET_KEY=your_flask_secret_key
```

## Dependencias Principales
```text
flask==3.0.2
python-dotenv==1.0.1
langchain==0.1.9
langchain-community==0.0.24
langchain-anthropic==0.1.1
langchain-openai==0.0.8
langchain-mistralai==0.0.3
anthropic==0.18.1
openai==1.12.0
mistralai>=0.0.11,<0.0.12
faiss-cpu==1.7.4
sentence-transformers==2.5.1
pypdf==4.1.0
```

## Uso
1. Iniciar la aplicación:
```bash
python app.py
```

2. Abrir el navegador y acceder a:
```
http://localhost:5000
```

3. Seleccionar el modelo de IA deseado
4. Realizar preguntas sobre los documentos cargados

## Estructura del Proyecto
```
rag-multillm/
├── static/
│   ├── css/
│   ├── js/
│   └── images/
├── templates/
├── uploads/
├── .env
├── app.py
├── config.py
├── rag.py
└── requirements.txt
```

## Características de los Modelos

### Claude 3 Sonnet
- Excelente comprensión contextual
- Respuestas detalladas y estructuradas
- Soporte multilingüe avanzado

### GPT-4 Turbo
- Alta precisión en respuestas
- Razonamiento complejo
- Versatilidad en tareas diversas

### Mistral Large
- Alto rendimiento y velocidad
- Excelente en análisis técnico
- Eficiente en recursos

## Contribución
Las contribuciones son bienvenidas. Por favor, sigue estos pasos:
1. Fork el repositorio
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Crea un Pull Request

## Licencia
Este proyecto está bajo la licencia MIT. Ver el archivo `LICENSE` para más detalles.

## Autor
@686f6c61

## Versión
v0.3 - Integración de múltiples modelos LLM
