// Esperar a que el DOM esté completamente cargado
document.addEventListener('DOMContentLoaded', function() {
    // Inicializar componentes de Material Design
    mdc.autoInit();

    function mostrarError(mensaje) {
        // Mostrar error en un toast o alert
        alert(mensaje);
    }

    function mostrarCargando(mostrar) {
        const loading = document.getElementById('loading');
        const btnPreguntar = document.getElementById('btnPreguntar');
        const preguntaTextarea = document.getElementById('pregunta');
        
        if (loading && btnPreguntar && preguntaTextarea) {
            // Mostrar/ocultar el spinner
            loading.style.display = mostrar ? 'flex' : 'none';
            
            // Deshabilitar/habilitar elementos durante la carga
            btnPreguntar.disabled = mostrar;
            preguntaTextarea.disabled = mostrar;
            
            // Actualizar clases y estilos
            if (mostrar) {
                btnPreguntar.classList.add('mdc-button--disabled');
                preguntaTextarea.classList.add('textarea--disabled');
                // Scroll al loader
                loading.scrollIntoView({ behavior: 'smooth', block: 'start' });
            } else {
                btnPreguntar.classList.remove('mdc-button--disabled');
                preguntaTextarea.classList.remove('textarea--disabled');
            }
        }
    }

    function contarPalabras(html) {
        // Crear un elemento temporal
        const temp = document.createElement('div');
        temp.innerHTML = html;
        
        // Obtener solo el texto, eliminando HTML
        const texto = temp.textContent || temp.innerText;
        
        // Contar palabras (dividir por espacios y filtrar elementos vacíos)
        const palabras = texto.trim().split(/\s+/).filter(word => word.length > 0);
        
        return palabras.length;
    }

    function mostrarRespuesta(data) {
        const respuestaDiv = document.getElementById('respuesta');
        const contenidoRespuesta = document.getElementById('contenido-respuesta');

        if (respuestaDiv && contenidoRespuesta) {
            // Limpiar contenido anterior
            contenidoRespuesta.innerHTML = '';
            
            if (data.respuesta) {
                // Contar palabras
                const numeroPalabras = contarPalabras(data.respuesta);
                
                // Crear el contenedor de la respuesta con el contador
                const contenedorCompleto = `
                    <div class="contenedor-respuesta">
                        ${data.respuesta}
                        <div class="contador-palabras">
                            <i class="material-icons">format_list_numbered</i>
                            <span>${numeroPalabras} palabras</span>
                        </div>
                    </div>
                `;
                
                // Insertar en el DOM
                contenidoRespuesta.innerHTML = contenedorCompleto;
                
                // Mostrar el contenedor
                respuestaDiv.style.display = 'block';
                
                // Reinicializar componentes de Material Design
                mdc.autoInit(contenidoRespuesta);
                
                // Scroll suave hasta la respuesta
                respuestaDiv.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        }
    }

    async function hacerPregunta() {
        const preguntaInput = document.getElementById('pregunta');
        const pregunta = preguntaInput?.value?.trim();

        if (!pregunta) {
            mostrarError('Por favor, escribe una pregunta');
            return;
        }

        try {
            // Mostrar loading y ocultar resultados anteriores
            mostrarCargando(true);
            document.getElementById('respuesta').style.display = 'none';

            // Realizar la petición al servidor
            const response = await fetch('/preguntar', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ pregunta: pregunta })
            });

            if (!response.ok) {
                throw new Error(`Error del servidor: ${response.status}`);
            }

            const data = await response.json();

            if (data.error) {
                throw new Error(data.error);
            }

            // Mostrar la respuesta
            mostrarRespuesta(data);

        } catch (error) {
            console.error('Error:', error);
            mostrarError(`Error: ${error.message}`);
        } finally {
            mostrarCargando(false);
        }
    }

    // Añadir evento para el botón
    const btnPreguntar = document.getElementById('btnPreguntar');
    if (btnPreguntar) {
        btnPreguntar.addEventListener('click', hacerPregunta);
    }

    // Añadir evento para Enter en el textarea
    const preguntaTextarea = document.getElementById('pregunta');
    if (preguntaTextarea) {
        preguntaTextarea.addEventListener('keypress', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                hacerPregunta();
            }
        });
    }
});

