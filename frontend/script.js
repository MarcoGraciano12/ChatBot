// const msgerForm = get(".msger-inputarea");
// const msgerInput = get(".msger-input");
const msgerChat = get(".msger-chat");
const BOT_IMG = "https://plus.unsplash.com/premium_vector-1727953895370-731b77162e13?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8ODd8fHVzZXJ8ZW58MHx8MHx8fDA%3D";
const PERSON_IMG = "https://plus.unsplash.com/premium_vector-1728555238545-2b26f9374b8e?q=80&w=2360&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D";
const BOT_NAME = "Asistente";
const PERSON_NAME = "Usuario";
const msgerForm = document.querySelector('.msger-inputarea');
const msgerInput = document.querySelector('#msgerInput');
const micButton = document.querySelector('#micButton');
let recognition;
let isRecording = false;

msgerForm.addEventListener('submit', event => {
  event.preventDefault();
  const msgText = msgerInput.value;
  if (!msgText) return;
  appendMessage(PERSON_NAME, PERSON_IMG, 'right', msgText);
  handleStream();
  msgerInput.value = '';
});

micButton.addEventListener('click', () => {
  if (isRecording) {
    recognition.stop();
    isRecording = false;
    micButton.innerHTML = '<span class="material-symbols-outlined">mic_off</span>';
  } else {
    recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = 'es-ES';
    recognition.start();
    isRecording = true;
    micButton.innerHTML = '<span class="material-symbols-outlined">cancel</span>';

    recognition.onresult = event => {
      const transcript = event.results[0][0].transcript;
      msgerInput.value = transcript;
      msgerForm.dispatchEvent(new Event('submit'));
    };

    recognition.onerror = event => {
      console.error('Speech recognition error:', event.error);
    };

    recognition.onend = () => {
      isRecording = false;
      micButton.innerHTML = '<span class="material-symbols-outlined">mic</span>';
    };
  }
});


// Lógica para los elementos del menú

// Variables para almacenar las selecciones
let formatListSelection = null;
let settingsSelection = null;

// Mapeo de acciones para los iconos del menú
const menuActions = {
  "cleaning_services": () => {
    msgerChat.innerHTML = "";
    appendMessage(BOT_NAME, BOT_IMG, "left", "Hola, ¡Bienvenido al ChatBot de NextAI Solutions! 😄");
  },
  "graph_4": async () => {
    try {
      const response = await fetch("http://127.0.0.1:5000/ollama/change-model");

      if (!response.ok) throw new Error("Error al obtener modelos");

      const data = await response.json();
      showModelSelectionModal(data.models);
    } catch (error) {
      console.error("Error:", error);
      alert("No se pudieron obtener los modelos.");
    }
  },
  "format_list_numbered": () => {
    showNumberSelectionModal("Selecciona un número (1-15)", 1, 15, (value) => {
      formatListSelection = value;
      console.log("Valor de format_list_numbered guardado:", formatListSelection);
    });
  },
  "settings": () => {
    showNumberSelectionModal("Selecciona un número (1-3)", 1, 3, (value) => {
      settingsSelection = value;
      console.log("Valor de settings guardado:", settingsSelection);
    });
  }
};

// Asignar eventos a cada icono del menú basado en `menuActions`
document.querySelectorAll(".material-symbols-outlined").forEach(icon => {
  const action = menuActions[icon.textContent.trim()];
  if (action) {
    icon.addEventListener("click", action);
  }
});

// Función para mostrar un modal de selección de modelos
function showModelSelectionModal(models) {
  createModal("Selecciona un modelo", models, async (selectedIndex) => {
    await changeModel(selectedIndex);
  });
}

// Función para cambiar de modelo mediante POST
async function changeModel(index) {
  try {
    const response = await fetch("http://127.0.0.1:5000/ollama/change-model", {

      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ index })
    });

    if (!response.ok) throw new Error("Error al cambiar de modelo");

    const data = await response.json();
    appendMessage(BOT_NAME, BOT_IMG, "left", data.message);
  } catch (error) {
    console.error("Error:", error);
    alert("No se pudo cambiar el modelo.");
  }
}

// Función para mostrar un modal de selección numérica
function showNumberSelectionModal(title, min, max, callback) {
  const options = Array.from({ length: max - min + 1 }, (_, i) => (i + min).toString());
  createModal(title, options, callback);
}

// Función genérica para crear modales con botones estilizados
function createModal(title, options, callback) {
  // Eliminar cualquier modal previo
  document.getElementById("customModal")?.remove();

  // Crear el modal con `innerHTML` para aplicar clases CSS
  const modal = document.createElement("div");
  modal.id = "customModal";
  modal.className = "modal"; // Aplicamos la clase "modal"

  modal.innerHTML = `
    <div class="brutalist-cd">

      <div class="brutalist-card__header">
   
        <div class="brutalist-card__alert">${title}</div>

      </div>

      <div class="brutalist-card__message">
         <select class="modal-select">
          ${options.map((option, index) => `<option value="${index}">${option}</option>`).join('')}
        </select>
      </div>

      <div class="brutalist-card__actions">
        <a class="brutalist-card__button brutalist-card__button--mark apply" href="#">Aplicar</a>
        <a class="brutalist-card__button brutalist-card__button--read cancel" href="#">Cancelar</a>
      </div>
      
    </div>
  `;

  // Agregar funcionalidad a los botones
  modal.querySelector(".apply").addEventListener("click", () => {
    const selectedValue = parseInt(modal.querySelector(".modal-select").value, 10);
    callback(selectedValue);
    modal.remove();
  });

  modal.querySelector(".cancel").addEventListener("click", () => {
    modal.remove(); // Cierra el modal sin hacer cambios
  });

  document.body.appendChild(modal);
}
// Fin de lógica para los elementos del menú

function appendMessage(name, img, side, text) {
  const msgHTML = `
      <div class="msg ${side}-msg ${name === BOT_NAME ? 'bot-msg' : ''}">
        <div class="msg-img" style="background-image: url(${img})"></div>
  
        <div class="msg-bubble">
          <div class="msg-info">
            <div class="msg-info-name">${name}</div>
            <div class="msg-info-time">${formatDate(new Date())}</div>
          </div>
  
          <div class="msg-text">${text}</div>
        </div>
      </div>
    `;
  msgerChat.insertAdjacentHTML("beforeend", msgHTML);
  msgerChat.scrollTop += 500;
}

async function handleStream() {
  // URL de tu API de streaming
  const apiUrl = 'http://127.0.0.1:5000/ollama';

  // Crear el objeto con los parámetros dinámicos
  const requestData = { query: msgerInput.value };
  console.log(">>> Query: ", msgerInput.value);

  // Agregar los valores solo si existen
  if (formatListSelection !== null) {
    requestData.rag = formatListSelection + 1;
    console.log(">>> RAG: ", formatListSelection + 1);
  }
  if (settingsSelection !== null) {
    requestData.level = settingsSelection;
    console.log(">>> Level: ", settingsSelection);
  }

  const response = await fetch(apiUrl, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(requestData)
  });

  if (!response.ok) {
    throw new Error('Error en la solicitud');
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let result = '';

  // Crear una nueva burbuja para cada pregunta del usuario (sin sobreescribir la anterior)
  appendMessage(BOT_NAME, BOT_IMG, 'left', ''); // Crea un mensaje vacío para la respuesta

  // Obtener la nueva burbuja del bot
  let botMessageElement = document.querySelector('.bot-msg:last-child');

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    // Acumulamos el resultado
    result += decoder.decode(value, { stream: true });

    // Actualizamos el contenido del mensaje del bot
    if (botMessageElement) {
      const botMessageText = botMessageElement.querySelector('.msg-text');
      if (botMessageText) {
        botMessageText.innerHTML = result;  // Acumula el texto dentro de la misma burbuja
      }
    }

    // Espera un breve momento para permitir la actualización del DOM y luego ajusta el scroll
    await new Promise(resolve => setTimeout(resolve, 50));
    msgerChat.scrollTop = msgerChat.scrollHeight;
  }
}

// Utils
function get(selector, root = document) {
  return root.querySelector(selector);
}

function formatDate(date) {
  const h = "0" + date.getHours();
  const m = "0" + date.getMinutes();

  return `${h.slice(-2)}:${m.slice(-2)}`;
}

function random(min, max) {
  return Math.floor(Math.random() * (max - min) + min);
}
