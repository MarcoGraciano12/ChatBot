document.addEventListener('DOMContentLoaded', () => {
    const dropArea = document.getElementById('drop-area');
    const fileInput = document.getElementById('file');
    const uploadIcon = document.getElementById('upload-icon');
    const deleteIcon = document.getElementById('delete-icon');
    const submitBtn = document.getElementById('submit-btn');
    const collectionNameInput = document.getElementById('msgerInput');
    const fileMessage = document.getElementById('file-message');

    // Drag and drop functionality
    dropArea.addEventListener('dragover', (event) => {
        event.preventDefault();
        dropArea.classList.add('dragover');
    });

    dropArea.addEventListener('dragleave', () => {
        dropArea.classList.remove('dragover');
    });

    dropArea.addEventListener('drop', (event) => {
        event.preventDefault();
        dropArea.classList.remove('dragover');
        const files = event.dataTransfer.files;
        if (files.length > 0) {
            fileInput.files = files;
            fileMessage.textContent = `Archivo seleccionado: ${files[0].name}`;
        }
    });

    // // Upload icon functionality
    // uploadIcon.addEventListener('click', () => {
    //     fileInput.click();
    // });

    fileInput.addEventListener('change', () => {
        if (fileInput.files.length > 0) {
            fileMessage.textContent = `Archivo seleccionado: ${fileInput.files[0].name}`;
        }
    });

    // Delete icon functionality
    deleteIcon.addEventListener('click', (event) => {
        event.preventDefault();
        if (fileInput.files.length > 0) {
            fileInput.value = '';
            fileMessage.textContent = 'Archivo eliminado';
        } else {
            fileMessage.textContent = 'No hay archivo seleccionado';
        }
    });

    // Submit button functionality
submitBtn.addEventListener('click', () => {
    if (submitBtn.disabled) return; // Evita múltiples clics

    const file = fileInput.files[0];
    const category = collectionNameInput.value;

    if (file && category) {
        submitBtn.disabled = true; // Deshabilitar el botón

        const formData = new FormData();
        formData.append('file', file);
        formData.append('category', category);

        fetch('http://127.0.0.1:5000/rag', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.status) { // Suponiendo que la API devuelve un "status: true" en éxito
                fileMessage.textContent = '✅ Archivo cargado exitosamente';
                
                // Limpiar el input de archivo después de mostrar el mensaje de éxito
                setTimeout(() => {
                    fileInput.value = '';
                    fileMessage.textContent = 'No hay archivo seleccionado';
                }, 3000); // Espera 3 segundos antes de limpiar el mensaje
            } else {
                fileMessage.textContent = '⚠️ Hubo un problema al guardar el archivo';
            }

            console.log('Success:', data);
        })
        .catch((error) => {
            fileMessage.textContent = '❌ Error al cargar el archivo';
            console.error('Error:', error);
        })
        .finally(() => {
            setTimeout(() => {
                submitBtn.disabled = false; // Rehabilitar el botón después de 3 segundos
            }, 3000);
        });
    } else {
        alert('Por favor, selecciona un archivo y proporciona un nombre para la colección.');
    }
});





});