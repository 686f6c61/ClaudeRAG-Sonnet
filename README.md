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


## Descripción de la Estructura del Proyecto

- **`__init__.py`**: Indica que el directorio `mi_rag_claude` es un paquete Python.
- **`main.py`**: Archivo principal que actúa como punto de entrada y proporciona una interfaz de línea de comandos (CLI) para interactuar con el sistema RAG.
- **`config.py`**: Contiene la configuración del proyecto y las variables de entorno necesarias para su funcionamiento.
- **`rag.py`**: Implementación del sistema **Retrieval-Augmented Generation (RAG)** que integra **Claude** y **Sonnet 2.5**.
- **`documentos/`**: Directorio destinado a almacenar archivos PDF que serán utilizados por el sistema RAG.
  - **`ejemplo.pdf`**: Un archivo PDF de ejemplo dentro del directorio `documentos`.

## Cómo Utilizar la Estructura

Esta estructura organizada facilita el mantenimiento y la escalabilidad del proyecto. Asegúrate de mantener una convención de nombres clara y comentarios descriptivos para cada archivo y directorio, lo que ayudará a otros colaboradores a entender rápidamente la funcionalidad de cada componente.

### Pasos Sugeridos

1. **Configuración Inicial**:
    - Edita `config.py` para establecer las variables de entorno necesarias, como claves API o rutas de acceso a recursos.

2. **Añadir Documentos**:
    - Coloca los archivos PDF que deseas procesar dentro del directorio `documentos/`.

3. **Ejecutar el Proyecto**:
    - Usa `main.py` para interactuar con el sistema RAG a través de la línea de comandos.

4. **Desarrollo y Extensiones**:
    - Modifica `rag.py` para ajustar la implementación del sistema RAG según tus necesidades específicas.
    - Añade funcionalidades adicionales en otros módulos según sea necesario.

## Ejemplo de Uso

```bash
python main.py --help



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
