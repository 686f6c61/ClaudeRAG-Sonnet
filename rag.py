# rag.py
import os
from typing import List, Dict
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from langchain_mistralai import ChatMistralAI
from langchain.chains import ConversationalRetrievalChain
from langchain.schema import Document
import config

def cargar_documentos(directorio: str = "documentos") -> List[Document]:
    """Carga todos los documentos PDF del directorio especificado"""
    loader = DirectoryLoader(
        directorio,
        glob="**/*.pdf",
        loader_cls=PyPDFLoader
    )
    return loader.load()

def crear_chunks(documentos: List[Document], 
                chunk_size: int = 1000, 
                chunk_overlap: int = 200) -> List[Document]:
    """Divide los documentos en chunks más pequeños"""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    return text_splitter.split_documents(documentos)

def crear_vectorstore(chunks: List[Document]) -> FAISS:
    """Crea una base de datos vectorial con los chunks"""
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )
    return FAISS.from_documents(chunks, embeddings)

def crear_llm(modelo: str = "claude"):
    """Crea el modelo de lenguaje según el tipo especificado"""
    if modelo == "claude":
        print(f"Inicializando Claude con clave API: {config.ANTHROPIC_API_KEY[:8]}...")  # Solo muestra los primeros 8 caracteres
        try:
            return ChatAnthropic(
                anthropic_api_key=config.ANTHROPIC_API_KEY,
                model_name="claude-3-sonnet-20240229",
                temperature=0.1,
                max_tokens=4096
            )
        except Exception as e:
            print(f"Error al inicializar Claude: {str(e)}")
            raise
    elif modelo == "gpt4":
        return ChatOpenAI(
            openai_api_key=config.OPENAI_API_KEY,
            model_name="gpt-4-turbo-preview",
            temperature=0.1,
            max_tokens=4096
        )
    elif modelo == "mistral":
        return ChatMistralAI(
            mistral_api_key=config.MISTRAL_API_KEY,
            model="mistral-large-latest",
            temperature=0.1,
            max_tokens=4096
        )
    else:
        raise ValueError(f"Modelo no soportado: {modelo}")

def crear_rag_system(modelo: str = "claude"):
    """
    Crea y configura el sistema RAG completo
    """
    try:
        # Cargar y procesar documentos
        documentos = cargar_documentos()
        chunks = crear_chunks(documentos)
        vectorstore = crear_vectorstore(chunks)
        
        # Crear LLM según el modelo seleccionado
        llm = crear_llm(modelo)
        
        # Crear y retornar el sistema RAG
        return ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
            return_source_documents=True,
            verbose=True
        )
    except Exception as e:
        print(f"Error creando el sistema RAG: {str(e)}")
        raise

def formatear_cita_apa(documento) -> str:
    """Formatea una cita en estilo APA"""
    # Extraer metadatos del documento
    source = documento.metadata.get('source', 'Documento sin título')
    filename = os.path.basename(source)
    name_without_ext = os.path.splitext(filename)[0]
    
    # Crear cita APA básica
    return f"{name_without_ext}. (s.f.). Página {documento.metadata.get('page', 'n/a')}."

def hacer_pregunta(qa_chain, pregunta: str, historial_chat: List = None) -> Dict:
    """
    Realiza una pregunta al sistema RAG y devuelve la respuesta formateada
    """
    if historial_chat is None:
        historial_chat = []

    prompt_template = """
    Por favor, proporciona una respuesta detallada y exhaustiva (mínimo 500 palabras) a la siguiente pregunta. 
    Tu respuesta debe seguir esta estructura HTML específica:

    <article class="respuesta-completa">
        <h2>[Título descriptivo y relevante]</h2>
        
        <div class="contenido">
            <h3>Introducción</h3>
            <p>[Contexto general y relevancia del tema]</p>
            
            <h3>Desarrollo Principal</h3>
            [Múltiples párrafos con subtemas]
            
            <h3>Aspectos Adicionales</h3>
            [Perspectivas alternativas o consideraciones importantes]
            
            <h3>Conclusión</h3>
            <p>[Resumen de puntos clave]</p>
        </div>
        
        <div class="tags">
            <span class="tag">#[tag1]</span>
            <span class="tag">#[tag2]</span>
            <span class="tag">#[tag3]</span>
        </div>
    </article>

    Pregunta: {pregunta}
    """

    try:
        # Realizar la consulta
        resultado = qa_chain({
            "question": prompt_template.format(pregunta=pregunta),
            "chat_history": historial_chat
        })
        
        # Procesar las fuentes
        citas_apa = set()
        for doc in resultado.get("source_documents", []):
            cita = formatear_cita_apa(doc)
            citas_apa.add(cita)

        # Crear sección de referencias
        referencias_html = f"""
        <section class="referencias">
            <h3>Referencias</h3>
            <ul class="referencias-lista">
                {''.join(f'<li class="referencia-item">{cita}</li>' for cita in sorted(citas_apa))}
            </ul>
        </section>
        """

        # Combinar respuesta y referencias
        respuesta_completa = f"""
        <div class="contenedor-respuesta">
            {resultado['answer']}
            {referencias_html}
        </div>
        """

        return {
            "respuesta": respuesta_completa,
            "fuentes": sorted(list(citas_apa))
        }
        
    except Exception as e:
        print(f"Error en hacer_pregunta: {str(e)}")
        raise