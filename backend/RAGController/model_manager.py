from RAGController.ollama_singleton import OllamaSingleton
import ollama


class ModelManager:
    """
    Clase encargada de gestionar y aplicar la configuración personalizada
    del usuario al modelo.
    """

    def __init__(self):
        # Se carga la lista de los modelos de Ollama disponibles.
        self.__available_models = self.load_models()

        # Variable para almacenar el modelo activo.
        self.__selected_model = None

        # Se obtiene la instancia de Ollama.
        self.ollama_instance = OllamaSingleton()

        # Se establece por defecto la cantidad de coincidencias del RAG a obtener.
        self._k = 1

        # Se establece por defecto la calidad de respuesta del modelo
        self._level = 0

        # Variable para gestionar la colección sobre la cual se realizarán las búsquedas.
        self._category = None

    @staticmethod
    def load_models():
        """
        Método destinado a obtener la lista de modelos de Ollama que se encuentran en
        local.
        """
        try:
            return [llm['model'] for llm in ollama.list()['models']]
        except Exception as error:
            print(f"Error al cargar la lista de modelos locales: {error}.")
            return []

    def get_list_models(self):
        """
        Método destinado a retornar la lista de modelos de Ollama que se encuentran en
        local
        """
        return self.__available_models

    def change_selected_model(self, index:int):
        try:
            if 0 <= index < len(self.__available_models):
                # Se asigna el nuevo modelo activo
                self.__selected_model = self.__available_models[index]
                return True, f"Se ha activado el modelo {self.__available_models[index]}."

            return False, f"El modelo seleccionado no se encuentra dentro de la lista de modelos disponibles."
        except Exception as error:
            print(f">>> Error al cambiar el modelo activo: {error}.")
            return False, "Ocurrió un error inesperado al intentar cambiar el modelo."

    def set_k(self, k:int):
        """
        Método para asignar un nuevo valor a la variable encargada de gestionar la
        cantidad de coincidencias del RAG.
        """
        self._k = k

    def set_level(self, level:int):
        """
        Método para asignar un nuevo valor a la variable encargada de gestionar la calidad
        de las respuestas del modelo.
        """
        self._level = level

    def set_category(self, category:str):
        """
        Método para asignar un nuevo valor a la variable encargada de gestionar
        la colección sobre la cual se realizarán las búsquedas en la base de datos.
        """
        self._category = category

    def get_selected_model(self):
        """
        Método para retornar al modelo activo.
        """
        return self.__selected_model

    def get_selected_category(self):
        """
        Método para retornar la categoría que se encuentra activa.
        """
        return self._category

    def get_k(self):
        """
        Método para retornar el número de coincidencias del RAG a obtener.
        """
        return self._k

    def get_level(self):
        """
        Método para retornar el nivel de respueta del modelo.
        """
        return self._level