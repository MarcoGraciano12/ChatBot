document.addEventListener("DOMContentLoaded", function () {
    const combobox = document.getElementById("combobox");
    const submitBtn = document.getElementById("submit-btn");
    const statusIcon = document.querySelector(".user-picture span");
    const statusText = document.querySelector(".name-client");

    // Cargar las colecciones disponibles en el select
    async function loadCollections() {
        try {
            const response = await fetch("http://127.0.0.1:5000/rag");
            const data = await response.json();

            if (data.categories && data.categories.length > 0) {
                combobox.innerHTML = '<option value="0">Selecciona una opción</option>';
                data.categories.forEach(category => {
                    const option = document.createElement("option");
                    option.value = category;
                    option.textContent = category;
                    combobox.appendChild(option);
                });
            } else {
                combobox.innerHTML = '<option value="0">No hay colecciones disponibles</option>';
            }
        } catch (error) {
            console.error("Error al cargar colecciones:", error);
        }
    }

    // Manejar la eliminación de la colección seleccionada
    async function deleteCollection() {
        const selectedValue = combobox.value;
        
        if (selectedValue === "0") {
            alert("Selecciona una colección válida.");
            return;
        }

        try {
            const response = await fetch("http://127.0.0.1:5000/rag", {
                method: "DELETE",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ category: selectedValue })
            });

            const data = await response.json();

            if (data.status) {
                statusIcon.textContent = "check_circle"; // Icono de éxito
                statusText.textContent = "Colección eliminada con éxito.";
                loadCollections(); // Recargar las colecciones disponibles
            } else {
                statusIcon.textContent = "error"; // Icono de error
                statusText.textContent = "No se logró eliminar la colección.";
            }
        } catch (error) {
            console.error("Error al eliminar la colección:", error);
            statusIcon.textContent = "error"; // Icono de error
            statusText.textContent = "Ocurrió un error inesperado.";
        }
    }

    // Eventos
    submitBtn.addEventListener("click", deleteCollection);
    loadCollections(); // Cargar colecciones al cargar la página
});
