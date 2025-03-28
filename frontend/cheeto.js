// Declaración de variables
const msgerChat = get(".msger-chat");
const BOT_NAME = "Asistente";
const PERSON_NAME = "Usuario";
const msgerForm = document.querySelector('.msger-inputarea');
const msgerInput = document.querySelector('#msgerInput');
const micButton = document.querySelector('#micButton');

let messageHistory = [];
let historyIndex = -1;





let recognition;
let isRecording = false;
let selectedCategorySelection = null;
// Variables para almacenar las selecciones
let formatListSelection = null;
let settingsSelection = null;
const BOT_IMG = "https://plus.unsplash.com/premium_vector-1727952230168-809436181c0c?q=80&w=1760&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D";
const PERSON_IMG = "https://plus.unsplash.com/premium_vector-1728572090497-ca25df7e50cf?q=80&w=1760&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D";


// Función para obtener el recurso solicitado
function get(selector, root = document) {
  return root.querySelector(selector);
}

//   Función para obtener la hora 
function formatDate(date) {
  const h = "0" + date.getHours();
  const m = "0" + date.getMinutes();

  return `${h.slice(-2)}:${m.slice(-2)}`;
}

// Para el evento de funcionalidad del menú
document.addEventListener("DOMContentLoaded", function () {
  const toggleMenu = document.querySelector(".header-container div span");
  const menuContainer = document.querySelector(".contenedor-menu");

  toggleMenu.addEventListener("click", function () {
    menuContainer.classList.toggle("contraido");
  });
});

// Función para agregar un texto al chat 
function appendMessage(name, img, side, text) {
  const msgHTML = `
        <div class="msg ${side}-msg ${name === BOT_NAME ? 'bot-msg' : ''}">
          <div class="msg-img" style="background-image: url(${img})"></div>
    
          <div class="msg-bubble">
            <div class="msg-info">
              <div class="msg-info-name tinos-bold">${name}</div>
              <div class="msg-info-time tinos-bold">${formatDate(new Date())}</div>
            </div>
    
            <div class="msg-text tinos-regular">${text}</div>
          </div>
        </div>
      `;
  msgerChat.insertAdjacentHTML("beforeend", msgHTML);
  msgerChat.scrollTop += 500;
}


// Para la funcionalidad de personalización de la configuración del chat 

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
    showNumberSelectionModal("Precisión del Modelo", 1, 20, (value) => {
      formatListSelection = value;
      console.log("Valor de format_list_numbered guardado:", formatListSelection);
    });
  },
  "candlestick_chart": () => {
    // Mostrar palabras "Simple", "Normal", "Complejo" pero obtener el índice (0, 1, 2)
    showTextSelectionModal("Nivel de respuesta del modelo", ["Simple", "Normal", "Complejo"], (selectedIndex) => {
      settingsSelection = selectedIndex; // Obtener el índice (0, 1, 2)
      console.log("Valor de settings guardado:", settingsSelection);
    });
  },
  "file_copy": async () => {
    await fetchCategories();
  }
};

// Asignar eventos a cada icono del menú basado en `menuActions`
document.querySelectorAll(".material-symbols-outlined").forEach(icon => {
  const action = menuActions[icon.textContent.trim()];
  if (action) {
    icon.addEventListener("click", action);
  }
});

// Para la funcionalidad de los botones de enviar y grabar 
msgerForm.addEventListener('submit', event => {
  event.preventDefault();
  const msgText = msgerInput.value.trim();
  if (!msgText) return;

  // Guardar en historial
  messageHistory.push(msgText);
  historyIndex = messageHistory.length;

  // Verificar si hay categoría seleccionada
  if (!selectedCategorySelection) {
    alert("Debes seleccionar una categoría antes de hacer una consulta.");
    return;
  }
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
     
          <div class="brutalist-card__alert tinos-bold">${title}</div>
  
        </div>
  
        <div class="brutalist-card__message">
           <select class="modal-select tinos-bold-italic">
            ${options.map((option, index) => `<option value="${index}">${option}</option>`).join('')}
          </select>
        </div>
  
        <div class="brutalist-card__actions">
          <a class="brutalist-card__button brutalist-card__button apply tinos-bold" href="#">Aplicar</a>
          <a class="brutalist-card__button brutalist-card__button cancel tinos-bold" href="#">Cancelar</a>
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


// Función para mostrar un modal de selección de texto (palabras) pero obtener el índice
function showTextSelectionModal(title, options, callback) {
  // Crear el modal con las opciones
  createModal(title, options, (selectedIndex) => {
    callback(selectedIndex); // Pasar el índice al callback
  });
}


// Función para mostrar un modal de selección numérica
function showNumberSelectionModal(title, min, max, callback) {
  const options = Array.from({ length: max - min + 1 }, (_, i) => (i + min).toString());
  createModal(title, options, callback);
}


// Función para mostrar un modal con las categorías disponibles
function showCategorySelectionModal(categories) {
  createModal("Selecciona un Entrenamiento", categories, (selectedIndex) => {
    selectedCategorySelection = categories[selectedIndex];
    console.log("Entrenamiento seleccionada:", selectedCategorySelection);
  });
}

// Función para obtener las categorías desde la API
async function fetchCategories() {
  try {
    const response = await fetch("http://127.0.0.1:5000/rag");
    if (!response.ok) throw new Error("Error al obtener categorías");

    const data = await response.json();
    if (data.categories && data.categories.length > 0) {
      showCategorySelectionModal(data.categories);
    } else {
      alert("No hay categorías disponibles.");
    }
  } catch (error) {
    console.error("Error:", error);
    alert("No se pudieron obtener las categorías.");
  }
}

//Función para recibir stream de respuesta
async function handleStream() {

  // URL de tu API de streaming
  const apiUrl = 'http://127.0.0.1:5000/ollama';

  // Crear el objeto con los parámetros dinámicos
  const requestData = {
    query: msgerInput.value,
    category: selectedCategorySelection
  };

  console.log(">>> Query: ", msgerInput.value);
  console.log(">>> Categoría seleccionada: ", selectedCategorySelection);

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




msgerInput.addEventListener('keydown', event => {
  if (event.key === 'ArrowUp') {
    if (historyIndex > 0) {
      historyIndex--;
      msgerInput.value = messageHistory[historyIndex];
    }
    event.preventDefault();
  } else if (event.key === 'ArrowDown') {
    if (historyIndex < messageHistory.length - 1) {
      historyIndex++;
      msgerInput.value = messageHistory[historyIndex];
    } else {
      historyIndex = messageHistory.length;
      msgerInput.value = '';
    }
    event.preventDefault();
  }
});



// ===============================================================================================================================
//                                                     Funcionalidad de Entrenamiento
// ===============================================================================================================================
document.getElementById('chatbot').addEventListener('click', function() {
  var chats = document.getElementsByClassName("opcion1");
  var tools = document.getElementsByClassName("opcion2")[0];

  let chatsVisibles = Array.from(chats).some(chat => chat.style.display !== 'none' && chat.style.display !== '');

  if (chatsVisibles) {
      // Si hay chats visibles, ocultarlos
      Array.from(chats).forEach(chat => chat.style.display = 'none');
  } else {
      // Si están ocultos, mostrarlos
      Array.from(chats).forEach(chat => chat.style.display = '');
  }

  // No ocultar herramientas si ya están visibles en otra acción
  if (tools.style.display !== 'none') {
      tools.style.display = 'none';
  }
});

document.getElementById('entrenar').addEventListener('click', function() {
  var chats = document.getElementsByClassName("opcion1");
  var tools = document.getElementsByClassName("opcion2")[0];

  let toolsVisible = tools.style.display !== 'none' && tools.style.display !== '';

  // Siempre ocultamos los chats al entrenar
  Array.from(chats).forEach(chat => chat.style.display = 'none');

  // Alternamos la visibilidad de tools
  tools.style.display = 'flex';
});
