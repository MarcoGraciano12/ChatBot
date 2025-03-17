const msgerForm = get(".msger-inputarea");
const msgerInput = get(".msger-input");
const msgerChat = get(".msger-chat");

const BOT_MSGS = [
  "Hi, how are you?",
  "Ohh... I can't understand what you trying to say. Sorry!",
  "I like to play games... But I don't know how to play!",
  "Sorry if my answers are not relevant. :))",
  "I feel sleepy! :("
];

// Icons made by Freepik from www.flaticon.com
const BOT_IMG = "https://plus.unsplash.com/premium_vector-1727953895370-731b77162e13?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8ODd8fHVzZXJ8ZW58MHx8MHx8fDA%3D";
const PERSON_IMG = "https://plus.unsplash.com/premium_vector-1728555238545-2b26f9374b8e?q=80&w=2360&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D";
const BOT_NAME = "BOT";
const PERSON_NAME = "USER";

msgerForm.addEventListener("submit", event => {
  event.preventDefault();

  const msgText = msgerInput.value;
  if (!msgText) return;

  appendMessage(PERSON_NAME, PERSON_IMG, "right", msgText);
//   botResponse();
handleStream();
  msgerInput.value = "";
});



function botResponse() {


const apiUrl = 'http://127.0.0.1:5000/rag/query';

// Datos que quieres enviar en la solicitud POST
const dataToSend = {
  query: msgerInput.value
};

// Realizar la solicitud POST a la API
fetch(apiUrl, {
  method: 'POST', // Cambiamos el método a POST
  headers: {
    'Content-Type': 'application/json' // Especificamos que los datos se envían en formato JSON
  },
  body: JSON.stringify(dataToSend) // Convertimos los datos a una cadena JSON
})
  .then(response => {
    if (!response.ok) {
      throw new Error('Error en la solicitud');
    }
    return response.json();
  })
  .then(data => {
    // Aquí puedes trabajar con los datos recibidos
    console.log(data);
    // Por ejemplo, puedes acceder a los resultados así:
    data.results.forEach(result => {
      console.log(result);
      appendMessage(BOT_NAME,BOT_IMG, "left", result)
    });
  })
  .catch(error => {
    console.error('Hubo un problema con la solicitud:', error);
  });
}



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
    const apiUrl = 'http://127.0.0.1:5000/ollama/chat';

    const response = await fetch(apiUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ query: msgerInput.value }) 
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
