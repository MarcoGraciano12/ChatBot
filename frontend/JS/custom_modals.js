//                              Funcionamiento de los modales personalizados
// =========================================================================================================

function createModal({ title, message, options, selectedValue, onApply }) {
    console.log(`Abriendo modal: ${title}`);

    // Cerrar cualquier modal existente antes de abrir uno nuevo
    const existingModal = document.getElementById('modal');
    const existingOverlay = document.getElementById('modal-overlay');
    if (existingModal) existingModal.remove();
    if (existingOverlay) existingOverlay.remove();
    
    const modalContainer = document.createElement('div');
    modalContainer.classList.add('modal-container');
    modalContainer.id = 'modal';

    const overlay = document.createElement('div');
    overlay.classList.add('modal-overlay');
    document.body.appendChild(overlay);

    modalContainer.innerHTML = `
        <div class="content">
            <span class="title tinos-bold">${title}</span>
            <div class="input-content">
                <select id="modal-select">
                    ${options.map(option => `
                        <option class="tinos-regular-italic" value="${option.value}" ${option.value == selectedValue ? 'selected' : ''}>
                            ${option.label}
                        </option>
                    `).join('')}
                </select>
            </div>
            <p class="message tinos-regular">${message}</p>
        </div>
        <div class="actions">
            <button class="apply button" type="button">Aplicar</button>
            <button class="cancel button" type="button">Cancelar</button>
        </div>
    `;

    document.body.appendChild(modalContainer);
    modalContainer.classList.add('active');

    document.querySelector('.cancel').addEventListener('click', () => closeModal(modalContainer, overlay));
    document.querySelector('.apply').addEventListener('click', () => {
        const selectedOption = document.getElementById('modal-select').value;
        console.log(`Opción seleccionada: ${selectedOption}`);
        onApply(selectedOption);
        closeModal(modalContainer, overlay);
    });
}

function closeModal(modal, overlay) {
    console.log("Cerrando modal");
    modal.remove();
    overlay.remove();
}

async function openTrainingSelectionModal() {
    console.log("Abriendo selección de entrenamiento");
    const trainings = await fetch('http://127.0.0.1:5000/collections').then(res => res.json());
    console.log("Entrenamientos disponibles:", trainings);
    const activeTraining = await fetch('http://127.0.0.1:5000/collection').then(res => res.json());
    console.log("Entrenamiento activo:", activeTraining);

    createModal({
        title: 'Selección de Entrenamiento',
        message: 'Selecciona un entrenamiento para activarlo.',
        options: trainings.response.map(t => ({ label: t, value: t })),
        selectedValue: activeTraining.status ? activeTraining.response : '',
        onApply: async (selected) => {
            console.log(`Aplicando entrenamiento: ${selected}`);
            await fetch('http://127.0.0.1:5000/collection', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ category: selected })
            });
        }
    });
}

async function openResponseLevelModal() {
    console.log("Abriendo nivel de respuesta");
    const responseLevel = await fetch('http://127.0.0.1:5000/level').then(res => res.json());
    console.log("Nivel de respuesta actual:", responseLevel);

    createModal({
        title: 'Nivel de Respuesta',
        message: 'Cuanto mayor sea el nivel, más detallada será la respuesta.',
        options: [
            { label: 'Breve', value: 0 },
            { label: 'Normal', value: 1 },
            { label: 'Extenso', value: 2 }
        ],
        selectedValue: responseLevel.status ? responseLevel.response : '',
        onApply: async (selected) => {
            console.log(`Aplicando nivel de respuesta: ${selected}`);
            await fetch('http://127.0.0.1:5000/level', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ level: Number(selected) })
            });
        }
    });
}

async function openPrecisionModal() {
    console.log("Abriendo selección de precisión");
    const precision = await fetch('http://127.0.0.1:5000/rag-k').then(res => res.json());
    console.log("Precisión actual:", precision);

    createModal({
        title: 'Precisión del Modelo',
        message: 'Cuanto mayor sea la precisión, mayor será el tiempo de respuesta.',
        options: Array.from({ length: 20 }, (_, i) => ({ label: i + 1, value: i + 1 })),
        selectedValue: precision.status ? precision.response : '',
        onApply: async (selected) => {
            console.log(`Aplicando precisión: ${selected}`);
            await fetch('http://127.0.0.1:5000/rag-k', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ k: Number(selected) })
            });
        }
    });
}

async function openModelSelectionModal() {
    console.log("Abriendo selección de modelo");
    const models = await fetch('http://127.0.0.1:5000/models').then(res => res.json());
    console.log("Modelos disponibles:", models);
    const activeModel = await fetch('http://127.0.0.1:5000/model').then(res => res.json());
    console.log("Modelo activo:", activeModel);

    createModal({
        title: 'Selección de Modelo',
        message: 'Selecciona un modelo para activarlo.',
        options: models.response.map((m, index) => ({ label: m, value: index })),
        selectedValue: activeModel.status ? models.response.indexOf(activeModel.response) : '',
        onApply: async (selected) => {
            console.log(`Aplicando modelo: ${models.response[selected]}`);
            await fetch('http://127.0.0.1:5000/model', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ index: Number(selected) })
            });
        }
    });
}





const change_category = document.querySelector('#category');

change_category.addEventListener('click',()=>{
    openTrainingSelectionModal();
}
)

const change_level = document.querySelector('#level');

change_level.addEventListener('click',()=>{
    openResponseLevelModal();
}
)

const change_rag = document.querySelector('#rag');

change_rag.addEventListener('click',()=>{
    openPrecisionModal();
}
)

const change_model = document.querySelector('#model');

change_model.addEventListener('click',()=>{
    openModelSelectionModal();
}
)


//                            Para las operaciones del entrenamiento
// =========================================================================================================

// Para obtener archivo 


// Agregar el modal al body al cargar la página

document.addEventListener("DOMContentLoaded", function () {
    let selectedFile = null; // Variable global para almacenar el archivo seleccionado
    const sendButton = document.getElementById("send-data");

    const modal = document.createElement("div");
    modal.id = "modal-wrapper";
    modal.style.display = "none";
    modal.style.position = "fixed";
    modal.style.top = "0";
    modal.style.left = "0";
    modal.style.width = "100vw";
    modal.style.height = "100vh";
    modal.style.justifyContent = "center";
    modal.style.alignItems = "center";

    modal.innerHTML = `
        <div class="modal-container drop-area-container" id="drop-area">
            <div class="drop-area-header">
                <span class="material-symbols-outlined" style="font-size: 70px;">cloud_upload</span>
            </div>
            <label for="file" class="drop-area-footer">
                <p id="file-message">Arrastra el Documento</p>
            </label>
            <input id="file" type="file" style="display: none;">
        </div>
    `;
    document.body.appendChild(modal);

    // Mostrar el modal al hacer clic en el botón
    document.getElementById("open-modal").addEventListener("click", function () {
        console.log("Abriendo el modal para arrastrar archivos...");
        modal.style.display = "flex";
    });

    // Cerrar el modal al hacer clic fuera de él
    modal.addEventListener("click", function (event) {
        console.log("Cerrando el modal para arrastrar archivos...");
        const dropArea = document.getElementById("drop-area");
        if (!dropArea.contains(event.target)) {
            modal.style.display = "none";
        }
    });

    // Funcionalidad de arrastrar y soltar
    const dropArea = document.getElementById("drop-area");

    dropArea.addEventListener("dragover", function (event) {
        event.preventDefault();
        dropArea.classList.add("dragover");
    });

    dropArea.addEventListener("dragleave", function () {
        dropArea.classList.remove("dragover");
    });

    dropArea.addEventListener("drop", function (event) {
        event.preventDefault();
        dropArea.classList.remove("dragover");
        const files = event.dataTransfer.files;
        console.log("Archivos arrastrados:", files);
        handleFiles(files);
    });

    function handleFiles(files) {
        const fileMessage = document.getElementById("file-message");
        if (files.length > 0) {
            selectedFile = files[0]; // Almacenar el archivo seleccionado en la variable global
            console.log("Archivo seleccionado:", selectedFile);
            fileMessage.textContent = `Archivo seleccionado: ${selectedFile.name}`;
        } else {
            selectedFile = null;
            console.log("No se seleccionó ningún archivo");
            fileMessage.textContent = "No se seleccionó ningún archivo";
        }
    }

    // Funcionalidad del botón de quitar selección
    document.getElementById("clear-selection").addEventListener("click", function () {
        console.log("Quitando elemento seleccionado...");
        const fileMessage = document.getElementById("file-message");

        if (selectedFile) {
            console.log("Archivo antes de limpiar:", selectedFile);
            selectedFile = null; // Limpiar la selección del archivo
            fileMessage.textContent = "Arrastra el Documento";
            console.log("Archivo después de limpiar:", selectedFile);
        }
    });


    // Funcionalidad para enviar los datos al endpoint
    document.getElementById("send-data").addEventListener("click", function () {

        if (sendButton.disabled) return; // Evita múltiples clics
     
        let category = document.getElementById("train-name").value;
        console.log(category)
       
        if (!selectedFile) {
            alert("Por favor, selecciona un archivo.");
            return;
        }
        if (!category) {
            alert("Por favor, proporciona un nombre de categoría.");
            return;
        }

        sendButton.disabled = true; // Deshabilitar el botón
        console.log("Enviando información...");
        const formData = new FormData();
        formData.append("file", selectedFile);
        formData.append("category", category);

        fetch("http://127.0.0.1:5000/collections", {
            method: "POST",
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            console.log("Respuesta del servidor:", data);
            alert(data.response);
            sendButton.disabled = false;
        })
        .catch(error => {
            console.error("Error al enviar los datos:", error);
            sendButton.disabled = false;
        });
    });


});

// Para notificar resultados de operación 

async function loadTrainings() {
    try {
        const response = await fetch('http://127.0.0.1:5000/collections');
        const data = await response.json();
        
        if (!data.status) {
            console.error("Error al obtener entrenamientos");
            return;
        }
        
        const select = document.getElementById("trainingSelect");
        select.innerHTML = ""; // Limpiar opciones previas
        
        data.response.forEach(training => {
            const option = document.createElement("option");
            option.value = training;
            option.textContent = training;
            select.appendChild(option);
        });
    } catch (error) {
        console.error("Error al cargar entrenamientos:", error);
    }
  }
  
  async function deleteTraining() {
    const select = document.getElementById("trainingSelect");
    const selectedTraining = select.value;
    
    if (!selectedTraining) {
        alert("Selecciona un entrenamiento para eliminar.");
        return;
    }
    
    try {
        const response = await fetch('http://127.0.0.1:5000/collections', {
            method: 'DELETE',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ category: selectedTraining })
        });
        
        const data = await response.json();
        
        if (data.status) {
            alert(`Entrenamiento eliminado: ${selectedTraining}`);
            loadTrainings(); // Recargar la lista de entrenamientos
        } else {
            alert("Error al eliminar el entrenamiento.");
        }
    } catch (error) {
        console.error("Error al eliminar el entrenamiento:", error);
    }
  }
  


  // Recargar entrenamientos cada vez que el usuario abre el select
  document.getElementById("trainingSelect").addEventListener("focus", loadTrainings);
  
  
  const delete_button = document.getElementById("delete-button");
  
  
  delete_button.addEventListener('click',()=>{
    deleteTraining();
  }
  )
  
