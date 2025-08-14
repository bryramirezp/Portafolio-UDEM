document.addEventListener('DOMContentLoaded', () => {
    const sendBtn = document.getElementById('send-btn');
    const promptInput = document.getElementById('prompt-input');
    const chatBox = document.getElementById('chat-box');
    const loadingIndicator = document.getElementById('loading-indicator');

    // URL de la API de Ollama. Usamos el nombre del contenedor 'ollama' como hostname.
    // Como la página se sirve desde Apache, el navegador intentará acceder a esta URL.
    // Si Apache y Ollama están en la misma red Docker, esto no funcionará directamente desde el navegador del cliente.
    // La solución es usar una URL proxy o la IP pública del host Docker.
    // Para este ejemplo, asumiremos que usaremos un proxy en el futuro, pero por ahora apuntamos a la IP del host Docker.
    // REEMPLAZA 'IP_DE_TU_MAQUINA_DOCKER' por la IP de la máquina donde corre Docker.
    const OLLAMA_API_URL = 'http://localhost:11434/api/generate';

    sendBtn.addEventListener('click', sendMessage);
    promptInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    async function sendMessage() {
        const prompt = promptInput.value.trim();
        if (!prompt) return;

        addMessage(prompt, 'user');
        promptInput.value = '';
        loadingIndicator.style.display = 'block'; // Mostrar indicador de carga

        try {
            const response = await fetch(OLLAMA_API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    model: "deepseek-coder", // Asegúrate de que el nombre del modelo sea correcto
                    prompt: prompt,
                    stream: false // Para obtener la respuesta completa de una vez
                }),
            });

            if (!response.ok) {
                throw new Error(`Error de red: ${response.statusText}`);
            }

            const data = await response.json();
            addMessage(data.response, 'assistant');

        } catch (error) {
            console.error('Error al contactar la API de Ollama:', error);
            addMessage(`Error: No se pudo conectar con el modelo. Detalles: ${error.message}`, 'assistant');
        } finally {
            loadingIndicator.style.display = 'none'; // Ocultar indicador de carga
        }
    }

    function addMessage(text, sender) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', sender);
        messageElement.textContent = text;
        chatBox.appendChild(messageElement);
        chatBox.scrollTop = chatBox.scrollHeight; // Auto-scroll hacia el último mensaje
    }
});