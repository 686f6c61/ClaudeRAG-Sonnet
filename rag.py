# rag.py
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_anthropic import ChatAnthropic
from langchain.chains import ConversationalRetrievalChain

def procesar_pdfs(directorio, pdfs_seleccionados):
    """
    Carga y procesa los archivos PDF seleccionados
    """
    chunks = []
    total_pdfs = len(pdfs_seleccionados)
    
    print("\nProcesando documentos:")
    print("="*50)
    
    for i, pdf in enumerate(pdfs_seleccionados, 1):
        try:
            print(f"[{i}/{total_pdfs}] Procesando: {pdf}")
            ruta_completa = os.path.join(directorio, pdf)
            
            # Cargar PDF
            loader = PyPDFLoader(ruta_completa)
            documentos = loader.load()
            
            # Dividir en chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                length_function=len,
                separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""]
            )
            chunks_pdf = text_splitter.split_documents(documentos)
            
            # Agregar metadatos adicionales
            for chunk in chunks_pdf:
                chunk.metadata["source"] = pdf
                chunk.metadata["order"] = i
            
            chunks.extend(chunks_pdf)
            print(f"✓ {pdf} procesado correctamente ({len(chunks_pdf)} fragmentos)")
            
        except Exception as e:
            print(f"✗ Error procesando {pdf}: {str(e)}")
    
    print(f"\nTotal de fragmentos procesados: {len(chunks)}")
    return chunks

def crear_rag(directorio_docs, api_key, pdfs_seleccionados):
    """
    Crea y configura el sistema RAG con múltiples documentos
    """
    print("\nInicializando sistema RAG...")
    print("="*50)
    
    # Configurar embeddings
    print("Cargando modelo de embeddings...")
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )
    
    # Procesar PDFs seleccionados
    chunks = procesar_pdfs(directorio_docs, pdfs_seleccionados)
    if not chunks:
        raise ValueError("No se pudo procesar ningún documento")
    
    # Crear base de datos vectorial
    print("\nCreando base de datos vectorial...")
    vectorstore = FAISS.from_documents(chunks, embeddings)
    print(f"Base de datos creada con {len(chunks)} fragmentos")
    
    # Configurar Claude
    print("\nConfigurando Claude 3 Sonnet...")
    llm = ChatAnthropic(
        model="claude-3-sonnet-20240229",
        anthropic_api_key=api_key,
        temperature=0.1
    )
    
    # Crear cadena RAG
    print("\nCreando cadena RAG...")
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 3}
        ),
        return_source_documents=True,
        verbose=True
    )
    
    return qa_chain

def formatear_cita_apa(doc):
    """
    Formatea la metadata del documento en estilo APA
    """
    try:
        # Extraer información del documento
        source = doc.metadata.get('source', 'Documento sin título')
        page = doc.metadata.get('page', '?')
        
        # Eliminar la extensión .pdf del nombre del archivo
        source = os.path.splitext(source)[0]
        
        # Formatear el título si está en formato path
        source = os.path.basename(source)
        
        # Formatear la cita en estilo APA
        return f"{source} (p. {page})"
    except Exception as e:
        print(f"Error al formatear cita APA: {e}")
        return "Referencia no disponible"

def hacer_pregunta(qa_chain, pregunta, historial_chat=[]):
    """
    Realiza una pregunta al sistema RAG y devuelve la respuesta formateada en HTML
    """
    prompt_template = """
    Por favor, proporciona una respuesta detallada y exhaustiva (mínimo 500 palabras) a la siguiente pregunta. 
    Tu respuesta debe:
    
    1. Comenzar con una introducción que contextualice el tema
    2. Desarrollar múltiples aspectos y perspectivas del tema
    3. Incluir ejemplos específicos cuando sea relevante
    4. Proporcionar explicaciones detalladas de conceptos clave
    5. Concluir con un resumen de los puntos principales
    
    Estructura tu respuesta siguiendo este formato HTML específico:

    <article class="respuesta-completa">
        <h2>[Título descriptivo y relevante]</h2>
        
        <div class="contenido">
            <h3>Introducción</h3>
            <p>[Contexto general y relevancia del tema]</p>
            
            <h3>Desarrollo Principal</h3>
            [Múltiples párrafos con subtemas, usando:
            - <p> para párrafos
            - <strong> para conceptos importantes
            - <ul>/<li> para listas
            - <blockquote> para citas o ejemplos destacados
            - <h4> para subtemas específicos]
            
            <h3>Aspectos Adicionales a Considerar</h3>
            [Perspectivas alternativas, casos especiales, o consideraciones importantes]
            
            <h3>Conclusión</h3>
            <p>[Resumen de los puntos clave y cierre]</p>
        </div>
        
        <div class="tags">
            <span class="tag">#[tag1]</span>
            <span class="tag">#[tag2]</span>
            <span class="tag">#[tag3]</span>
            <span class="tag">#[tag4]</span>
        </div>
    </article>

    IMPORTANTE:
    - La respuesta debe ser extensa y detallada (mínimo 500 palabras)
    - Usa lenguaje claro pero técnico cuando sea apropiado
    - Incluye múltiples perspectivas y matices del tema
    - Proporciona ejemplos concretos
    - Asegúrate de que cada sección tenga suficiente desarrollo
    - Utiliza los elementos HTML para una estructura clara y legible

    Pregunta: {pregunta}
    """

    # Realizar la consulta
    resultado = qa_chain({
        "question": prompt_template.format(pregunta=pregunta),
        "chat_history": historial_chat
    })
    
    # Procesar las fuentes y crear citas APA
    citas_apa = set()
    for doc in resultado["source_documents"]:
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
        "citas_apa": sorted(list(citas_apa))
    }