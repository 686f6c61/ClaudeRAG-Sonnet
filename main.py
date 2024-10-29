# main.py
from config import ANTHROPIC_API_KEY, DOCUMENTOS_DIR
from rag import crear_rag, hacer_pregunta
import sys

def mostrar_menu():
    print("\n" + "="*50)
    print("RAG con Anthropic - Claude 3 Sonnet")
    print("Desarrollado por 686f6c61 - github.com/686f6c61")
    print("="*50)
    print("\n1. Hacer una pregunta")
    print("2. Salir")
    print("\n" + "="*50)

def seleccionar_pdfs(pdfs):
    print("\n" + "="*50)
    print("Archivos PDF disponibles:")
    print("="*50)
    for i, pdf in enumerate(pdfs, 1):
        print(f"{i}. {pdf}")
    print(f"{len(pdfs) + 1}. Procesar todos los archivos")
    print("="*50)

    while True:
        try:
            seleccion = input("\nSeleccione los números de los archivos a procesar (separados por comas) o 'todos': ")
            if seleccion.lower() == 'todos' or seleccion == str(len(pdfs) + 1):
                return pdfs

            indices = [int(i.strip()) for i in seleccion.split(',')]
            archivos_seleccionados = []
            
            for idx in indices:
                if 1 <= idx <= len(pdfs):
                    archivos_seleccionados.append(pdfs[idx-1])
                else:
                    print(f"Número inválido: {idx}")
                    raise ValueError
                    
            if archivos_seleccionados:
                return archivos_seleccionados
            
        except ValueError:
            print("\nPor favor, ingrese números válidos separados por comas o 'todos'")

def verificar_directorio_documentos():
    """
    Verifica la existencia del directorio documentos y los PDFs dentro de él.
    Retorna una tupla (bool, str) con el estado y mensaje.
    """
    import os
    
    # Verificar si existe el directorio
    if not os.path.exists(DOCUMENTOS_DIR):
        try:
            os.makedirs(DOCUMENTOS_DIR)
            return False, f"""
╔══════════════════════ ERROR ══════════════════════╗
║ No se encontró el directorio 'documentos'.        ║
║ Se ha creado el directorio automáticamente en:    ║
║ {os.path.abspath(DOCUMENTOS_DIR)}                 ║
║                                                   ║
║ Por favor, sigue estos pasos:                     ║
║ 1. Coloca tus archivos PDF en el directorio      ║
║ 2. Ejecuta el programa nuevamente                 ║
╚═══════════════════════════════════════════════════╝
"""
        except Exception as e:
            return False, f"""
╔══════════════════════ ERROR ══════════════════════╗
║ No se pudo crear el directorio 'documentos'.      ║
║ Error: {str(e)}                                   ║
║                                                   ║
║ Por favor, verifica los permisos del sistema     ║
║ y crea el directorio manualmente en:             ║
║ {os.path.abspath(os.path.dirname(__file__))}     ║
╚═══════════════════════════════════════════════════╝
"""

    # Verificar archivos PDF
    pdfs = [f for f in os.listdir(DOCUMENTOS_DIR) if f.endswith('.pdf')]
    if not pdfs:
        return False, f"""
╔══════════════════════ ERROR ══════════════════════╗
║ No se encontraron archivos PDF en el directorio   ║
║ 'documentos'.                                     ║
║                                                   ║
║ Directorio actual:                               ║
║ {os.path.abspath(DOCUMENTOS_DIR)}                 ║
║                                                   ║
║ Por favor:                                        ║
║ 1. Agrega tus archivos PDF al directorio         ║
║ 2. Verifica que los archivos tengan              ║
║    extensión .pdf (en minúsculas)                ║
║ 3. Ejecuta el programa nuevamente                ║
╚═══════════════════════════════════════════════════╝
"""
    
    return True, pdfs

def main():
    # Verificar directorio y PDFs
    estado, resultado = verificar_directorio_documentos()
    if not estado:
        print(resultado)
        sys.exit(1)
    
    pdfs = resultado
    # Seleccionar PDFs a procesar
    pdfs_seleccionados = seleccionar_pdfs(pdfs)
    
    # Inicializar el sistema
    print("\nInicializando sistema RAG...")
    print("Procesando los siguientes PDFs:", ', '.join(pdfs_seleccionados))
    
    try:
        rag = crear_rag(DOCUMENTOS_DIR, ANTHROPIC_API_KEY, pdfs_seleccionados)
        print("\nSistema inicializado correctamente!")
    except Exception as e:
        print(f"Error al inicializar el sistema: {str(e)}")
        sys.exit(1)

    # Loop de conversación
    historial_chat = []
    while True:
        mostrar_menu()
        opcion = input("\nSeleccione una opción (1-2): ")
        
        if opcion == "1":
            try:
                pregunta = input("\nHaz tu pregunta: ")
                print("\nProcesando pregunta...")
                
                respuesta = hacer_pregunta(rag, pregunta, historial_chat)
                print("\nRespuesta:", respuesta["respuesta"])
                
                # Mostrar fuentes organizadas por documento
                print("\nFuentes utilizadas:")
                print("="*50)
                for pdf, docs in respuesta["fuentes_por_documento"].items():
                    print(f"\n📄 {pdf}:")
                    for i, doc in enumerate(docs, 1):
                        print(f"  {i}. Fragmento {doc.metadata.get('order', '?')}")
                
                # Actualizar historial
                historial_chat.append((pregunta, respuesta["respuesta"]))
                
                input("\nPresione Enter para continuar...")
                
            except Exception as e:
                print(f"\nError al procesar la pregunta: {str(e)}")
                input("\nPresione Enter para continuar...")
                
        elif opcion == "2":
            print("\n¡Gracias por usar el sistema RAG!")
            break
        else:
            print("\nOpción no válida. Por favor, seleccione 1 o 2.")
            input("\nPresione Enter para continuar...")

if __name__ == "__main__":
    main()