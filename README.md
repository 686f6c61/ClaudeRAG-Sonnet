# 🤖 RAG con Claude 3 Sonnet v0.2

## 📖 Descripción
Sistema de Recuperación Aumentada de Generación (RAG) implementado con Claude 3 Sonnet de Anthropic. Permite realizar consultas sobre documentos PDF a través de una interfaz web moderna, utilizando embeddings multilingües y una base de datos vectorial FAISS.

## 🛠️ Tecnologías

### Backend
- **LLM**: Claude 3 Sonnet (Anthropic)
- **Embeddings**: sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
- **Vector Store**: FAISS (Facebook AI Similarity Search)
- **Framework RAG**: LangChain
- **Servidor Web**: Flask
- **Procesamiento de Documentos**: PyPDF, RecursiveCharacterTextSplitter

### Frontend
- **Framework CSS**: Material Design (MDC Web Components)
- **Diseño**: Material UI con tema personalizado (azul/blanco)
- **JavaScript**: Vanilla JS con módulos
- **Fuentes**: Roboto, Material Icons

## 🆕 Nuevas Características v0.2
- **Interfaz Web Moderna**: Diseño responsive con Material Design
- **Formato HTML Enriquecido**: Respuestas estructuradas con títulos, párrafos y listas
- **Contador de Palabras**: Análisis automático de la extensión de respuestas
- **Referencias Mejoradas**: Citación APA con mejor formato visual
- **Loading States**: Indicadores visuales durante el procesamiento
- **Tags Temáticos**: Categorización automática de respuestas
- **Scroll Automático**: Mejor experiencia de usuario
- **Respuestas Extensas**: Mínimo 500 palabras por consulta

## 🔧 Instalación

### Prerrequisitos
- Python 3.8+
- pip
- Clave API de Anthropic
- Navegador web moderno

### Crear y activar entorno virtual
```bash
# Crear entorno
python -m venv venv

# Activar entorno
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### Instalar dependencias
```bash
pip install -r requirements.txt
```

### Variables de Entorno
Crear archivo `.env` en la raíz del proyecto:
```env
ANTHROPIC_API_KEY=tu_clave_de_api_de_anthropic
FLASK_SECRET_KEY=tu_clave_secreta_para_flask
```

## 📁 Estructura del Proyecto
```
mi_rag_claude/
├── static/
│   ├── css/
│   │   ├── main.css
│   │   └── components/
│   │       ├── header.css
│   │       ├── footer.css
│   │       ├── question.css
│   │       ├── response.css
│   │       └── loading.css
│   └── js/
│       └── app.js
├── templates/
│   └── index.html
├── documentos/
│   └── .pdf
├── init.py
├── app.py
├── config.py
├── rag.py
└── requirements.txt
```

## 🚀 Uso

1. Coloca tus archivos PDF en el directorio `documentos/`
2. Inicia el servidor Flask:
```bash
python app.py
```
3. Abre tu navegador en `http://localhost:5000`
4. Realiza consultas a través de la interfaz web

## 🔍 Características Técnicas
- Procesamiento selectivo de documentos PDF
- Interfaz web responsive
- Historial de chat
- Citación de fuentes en formato APA
- Embeddings multilingües
- Chunking inteligente de documentos
- Respuestas formateadas en HTML
- Contador de palabras automático

## ⚙️ Parámetros de Configuración
- **Chunk Size**: 1000 caracteres
- **Chunk Overlap**: 200 caracteres
- **Temperature**: 0.1
- **Top K**: 3 documentos similares
- **Palabras mínimas**: 500 por respuesta

## 📦 Dependencias Principales
```
flask==3.0.2
python-dotenv==1.0.1
langchain==0.1.9
langchain-community==0.0.24
langchain-anthropic==0.1.1
anthropic==0.18.1
faiss-cpu==1.7.4
sentence-transformers==2.5.1
pypdf==4.1.0
```

## 🤝 Contribuciones
Las contribuciones son bienvenidas. Por favor, abre un issue primero para discutir los cambios que te gustaría realizar.

## 📄 Licencia
MIT License

## 👤 Autor
[686f6c61](https://github.com/686f6c61)

## ⚠️ Disclaimer
Este proyecto utiliza la API de Anthropic. Asegúrate de cumplir con sus términos de servicio y políticas de uso.

## 🔗 Enlaces Útiles
- [Documentación de Claude](https://docs.anthropic.com/claude/docs)
- [LangChain](https://python.langchain.com/docs/get_started/introduction.html)
- [FAISS](https://github.com/facebookresearch/faiss)
- [Material Design](https://material.io/develop/web)
- [Flask](https://flask.palletsprojects.com/)
