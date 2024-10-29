# 🤖 RAG con Claude 3 Sonnet

## 📖 Descripción
Sistema de Recuperación Aumentada de Generación (RAG) implementado con Claude 3 Sonnet 2.5 de Anthropic. Permite realizar consultas sobre documentos PDF utilizando embeddings multilingües y una base de datos vectorial FAISS.

## 🛠️ Tecnologías
- **LLM**: Claude 3 Sonnet (Anthropic)
- **Embeddings**: sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
- **Vector Store**: FAISS (Facebook AI Similarity Search)
- **Framework**: LangChain
- **Procesamiento de Documentos**: PyPDF, RecursiveCharacterTextSplitter

## 🔧 Instalación

### Prerrequisitos
- Python 3.8+
- pip
- Clave API de Anthropic

### Crear entorno virtual

python -m venv venv

### Activar entorno virtual
source venv/bin/activate # Linux/Mac
venv\Scripts\activate # Windows

### Instalar dependencias

pip install -r requirements.txt


### Variables de Entorno
Crear archivo `.env` en la raíz del proyecto:

ANTHROPIC_API_KEY=tu_clave_de_api_de_anthropic


## 📁 Estructura del Proyecto


mi_rag_claude/
├── init.py
├── main.py # Punto de entrada y CLI
├── config.py # Configuración y variables de entorno
├── rag.py # Implementación del sistema RAG
└── documentos/ # Directorio para PDFs
    └── .pdf


## 🚀 Uso

1. Coloca tus archivos PDF en el directorio `documentos/`
2. Ejecuta el programa:

```bash
python3 main.py
```
3. Selecciona los PDFs a procesar
4. Realiza consultas sobre el contenido de los documentos

## 🔍 Características
- Procesamiento selectivo de documentos PDF
- Interfaz CLI intuitiva
- Historial de chat
- Citación de fuentes
- Embeddings multilingües
- Chunking inteligente de documentos

## ⚙️ Parámetros de Configuración
- **Chunk Size**: 1000 caracteres
- **Chunk Overlap**: 200 caracteres
- **Temperature**: 0.1
- **Top K**: 3 documentos similares

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
