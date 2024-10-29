# rag.py
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_anthropic import ChatAnthropic
from langchain.chains import ConversationalRetrievalChain

def procesar_pdfs(directorio):
    """
    Carga y procesa todos los archivos PDF en el directorio especificado
    """
    # Cargar PDFs
    loader = DirectoryLoader(
        directorio, 
        glob="**/*.pdf",
        loader_cls=PyPDFLoader
    )
    documentos = loader.load()
    
    # Dividir en chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""]
    )
    chunks = text_splitter.split_documents(documentos)
    
    return chunks

def crear_rag(directorio_docs, api_key, pdfs_seleccionados):
    """
    Crea y configura el sistema RAG
    """
    # Configurar embeddings
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )
    
    # Cargar solo los PDFs seleccionados
    chunks = []
    for pdf in pdfs_seleccionados:
        loader = PyPDFLoader(os.path.join(directorio_docs, pdf))
        documentos = loader.load()
        
        # Dividir en chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""]
        )
        chunks.extend(text_splitter.split_documents(documentos))
    
    # Crear base de datos vectorial
    vectorstore = FAISS.from_documents(chunks, embeddings)
    
    # Configurar Claude
    llm = ChatAnthropic(
        model="claude-3-sonnet-20240229",
        anthropic_api_key=api_key,
        temperature=0.1
    )
    
    # Crear cadena RAG
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

def hacer_pregunta(qa_chain, pregunta, historial_chat=[]):
    """
    Realiza una pregunta al sistema RAG
    """
    resultado = qa_chain({
        "question": pregunta,
        "chat_history": historial_chat
    })
    
    return {
        "respuesta": resultado["answer"],
        "documentos_fuente": resultado["source_documents"]
    }