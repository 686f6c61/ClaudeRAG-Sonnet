// Variables globales
let selectedModel = null;

document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM Cargado'); // Debug
    
    // Inicializar componentes de Material Design
    mdc.autoInit();

    // Ocultar el preloader inicialmente
    const loading = document.getElementById('loading');
    if (loading) {
        loading.style.display = 'none';
    }

    // Inicializar selector de modelo
    initializeModelSelector();

    // Inicializar eventos del formulario de pregunta
    initializeQuestionForm();
});

function initializeModelSelector() {
    console.log('Inicializando selector de modelo'); // Debug
    
    const modelCards = document.querySelectorAll('.model-card');
    const questionContainer = document.querySelector('.question-container');

    console.log('Número de model-cards encontradas:', modelCards.length); // Debug

    if (questionContainer) {
        questionContainer.style.display = 'none';
    }

    modelCards.forEach(card => {
        const btn = card.querySelector('.select-model-btn');
        if (btn) {
            btn.addEventListener('click', function(e) {
                console.log('Botón de modelo clickeado:', this.dataset.model); // Debug
                e.preventDefault();
                e.stopPropagation();
                const model = this.dataset.model;
                selectModel(model, card);
            });
        }
    });
}

function selectModel(model, selectedCard) {
    console.log('Seleccionando modelo:', model); // Debug
    
    // Actualizar UI
    document.querySelectorAll('.model-card').forEach(card => {
        card.classList.remove('selected');
    });
    selectedCard.classList.add('selected');
    
    // Guardar modelo seleccionado
    selectedModel = model;
    
    // Mostrar contenedor de preguntas
    const questionContainer = document.querySelector('.question-container');
    if (questionContainer) {
        questionContainer.style.display = 'block';
        questionContainer.scrollIntoView({ behavior: 'smooth' });
    }
}

function initializeQuestionForm() {
    console.log('Inicializando formulario de pregunta'); // Debug
    
    const btnPreguntar = document.getElementById('btnPreguntar');
    const preguntaTextarea = document.getElementById('pregunta');

    if (btnPreguntar) {
        btnPreguntar.addEventListener('click', function(e) {
            console.log('Botón preguntar clickeado'); // Debug
            e.preventDefault();
            hacerPregunta();
        });
    }

    if (preguntaTextarea) {
        preguntaTextarea.addEventListener('keypress', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                console.log('Enter presionado en textarea'); // Debug
                e.preventDefault();
                hacerPregunta();
            }
        });
    }
}

async function hacerPregunta() {
    console.log('Ejecutando hacerPregunta'); // Debug
    console.log('Modelo seleccionado:', selectedModel); // Debug

    if (!selectedModel) {
        mostrarError('Por favor, selecciona un modelo de IA primero');
        return;
    }

    const preguntaInput = document.getElementById('pregunta');
    const pregunta = preguntaInput?.value?.trim();

    if (!pregunta) {
        mostrarError('Por favor, escribe una pregunta');
        return;
    }

    try {
        console.log('Enviando pregunta al servidor...'); // Debug
        mostrarCargando(true);
        document.getElementById('respuesta').style.display = 'none';

        const response = await fetch('/preguntar', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                pregunta: pregunta,
                modelo: selectedModel 
            })
        });

        console.log('Respuesta recibida del servidor'); // Debug

        if (!response.ok) {
            throw new Error(`Error del servidor: ${response.status}`);
        }

        const data = await response.json();
        console.log('Datos recibidos:', data); // Debug

        if (data.error) {
            throw new Error(data.error);
        }

        mostrarRespuesta(data);

    } catch (error) {
        console.error('Error:', error);
        mostrarError(`Error: ${error.message}`);
    } finally {
        mostrarCargando(false);
    }
}

function mostrarCargando(mostrar) {
    const loading = document.getElementById('loading');
    const btnPreguntar = document.getElementById('btnPreguntar');
    const preguntaTextarea = document.getElementById('pregunta');
    
    if (loading && btnPreguntar && preguntaTextarea) {
        loading.style.display = mostrar ? 'flex' : 'none';
        btnPreguntar.disabled = mostrar;
        preguntaTextarea.disabled = mostrar;
        
        if (mostrar) {
            btnPreguntar.classList.add('mdc-button--disabled');
        } else {
            btnPreguntar.classList.remove('mdc-button--disabled');
        }
    }
}

function mostrarError(mensaje) {
    console.error('Error:', mensaje); // Debug
    alert(mensaje);
}

function mostrarRespuesta(data) {
    console.log('Mostrando respuesta:', data); // Debug
    const respuestaDiv = document.getElementById('respuesta');
    const contenidoRespuesta = document.getElementById('contenido-respuesta');

    if (respuestaDiv && contenidoRespuesta && data.respuesta) {
        contenidoRespuesta.innerHTML = data.respuesta;
        respuestaDiv.style.display = 'block';
        respuestaDiv.scrollIntoView({ behavior: 'smooth' });
    }
}

