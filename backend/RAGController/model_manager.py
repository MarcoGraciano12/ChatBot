"""
Módulo encargado de la gestión de modelos locales de Ollama para su uso dentro del sistema RAG.

Este módulo proporciona la clase `ModelManager`, que permite cargar, seleccionar y configurar modelos
de lenguaje grande (LLM) instalados localmente a través de Ollama. También gestiona parámetros relacionados
con la calidad de respuesta, la cantidad de coincidencias relevantes a recuperar (`k`) y la categoría o colección
sobre la cual se realizarán las búsquedas.
"""
from RAGController.ollama_singleton import OllamaSingleton
import ollama


class ModelManager:
    """
    Clase para gestionar modelos LLM locales disponibles mediante Ollama y configurar sus parámetros de uso.

    Esta clase permite:
    - Cargar la lista de modelos instalados localmente.
    - Seleccionar el modelo activo a utilizar.
    - Establecer parámetros de configuración como:
        - Nivel de precisión o profundidad en la respuesta del modelo.
        - Número de resultados relevantes (`k`) que debe recuperar el sistema RAG.
        - Categoría o colección temática para contextualizar las respuestas.
    """

    def __init__(self):
        # Se carga la lista de los modelos de Ollama disponibles.
        self.__available_models = self.load_models()['content']

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
        Método encargado de retornar la lista de modelos de Ollama que se encuentran disponibles en local.

        Returns:
            dict: Un diccionario con el estado, mensaje y resultado de la operación.
                - 'status' (bool): Estado de la operación.
                - 'message' (str): Mensaje de éxito o error.
                - 'content' (list): Lista con los modelos de Ollama disponibles.
        """
        try:

            return {'status': True, 'message': 'Se obtuvo de manera correcta la lista de modelos.',
                    'content': [llm['model'] for llm in ollama.list()['models']]}

        except Exception as error:
            return {'status': False, 'message': f'Ocurrió un error al cargar la lista de modelos: {str(error)}.',
                    'content': []}

    def get_list_models(self):
        """
        Método destinado a retornar la lista de modelos de Ollama que se encuentran en
        local
        """
        return self.__available_models

    def change_selected_model(self, index:int):
        """
        Método encargado de cambiar el modelo seleccionado para responder a las preguntas del usuario.

        Args:
            index (int): Indice que el modelo ocupa en la lista de modelos disponibles.

        Returns:
            dict: Un diccionario con el estado, mensaje y resultado de la operación.
                - 'status' (bool): Estado de la operación.
                - 'message' (str): Mensaje de éxito o error.
        """
        try:
            if 0 <= index < len(self.__available_models):
                # Se asigna el nuevo modelo activo
                self.__selected_model = self.__available_models[index]
                return {'status': True, 'message': f'Se ha activado el modelo {self.__available_models[index]}.'}

            # Si no se puede cambiar el modelo
            return {'status': False,
                    'message': 'El modelo seleccionado no se encuentra dentro de la lista de modelos disponibles.'}

        except Exception as error:
            return {'status': False, 'message': f'Ocurrió´un error al intentar cambiar el modelo: {str(error)}'}

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