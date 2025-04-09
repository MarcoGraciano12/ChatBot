"""
chat_session.py

Módulo principal que gestiona la sesión de interacción entre el usuario, el modelo LLM (Ollama) y la base de datos vectorial (Chroma).

Este módulo define la clase ChatSession, la cual sirve como fachada para controlar:
    - Selección y configuración del modelo LLM.
    - Gestión de colecciones en la base de datos de embeddings.
    - Ejecución de consultas al modelo con contexto aumentado por recuperación (RAG).
    - Validación de parámetros antes de cada interacción.

Requiere los módulos:
    - model_manager: Controlador del modelo LLM (cambio, configuración, consulta).
    - chroma_db_manager: Controlador de la base de datos vectorial y colecciones.

"""

# Importación de Módulos
from RAGController.model_manager import ModelManager
from RAGController.chroma_db_manager import ChromaDBManager
import re


class ChatSession:
    """
    Clase que centraliza y administra la lógica de interacción con un modelo LLM de Ollama
    y una base de datos vectorial gestionada con ChromaDB.

    Esta clase ofrece una interfaz unificada para controlar:
        - Modelos LLM disponibles y seleccionados.
        - Parámetros de configuración como nivel de respuesta y número de coincidencias (k).
        - Colecciones de datos (entrenamientos) para el sistema RAG.
        - Ejecución de consultas con recuperación aumentada (RAG) y generación de respuestas.

    """

    def __init__(self):
        self._model_manager = ModelManager()
        self.db_manager = ChromaDBManager()

    # Obtener lista de modelos disponibles.
    def get_available_models(self):
        """
        Método que retorna la lista de modelos disponibles de Ollama.

        Returns:
            list: Una lista que contiene los modelos de Ollama disponibles en local.
        """
        return self._model_manager.get_list_models()

    # Obtener el modelo activo.
    def get_active_model(self):
        """
        Método que retorna al modelo que se encuentre activado.

        Returns:
            dict: Un diccionario con el estado, mensaje y resultado de la operación.
                - 'status' (bool): Estado de la operación.
                - 'message' (str): Mensaje de éxito o error.
                - 'content' (str): El nombre del modelo seleccionado.
        """
        model = self._model_manager.get_selected_model()

        if not model:
            return {'status': False, 'message': 'No se ha seleccionado un modelo.'}

        return {'status': True, 'message': 'Se ha obtenido el modelo seleccionado', 'content': model}

    # Cambiar Modelo
    def change_model(self, index: int):
        """
        Método que permite cambiar el modelo activo según el usuario indique.

        Returns:
            dict: Un diccionario con el estado, mensaje y resultado de la operación.
                - 'status' (bool): Estado de la operación.
                - 'message' (str): Mensaje de éxito o error.
        """
        return self._model_manager.change_selected_model(index)

    # Obtener lista de colecciones disponibles.
    def get_available_collections(self):
        """
        Método encargado de retornar la lista de colecciones disponibles en la base de datos.

        Returns:
            list: Una lista con las colecciones (entrenamientos) disponibles.
        """
        return self.db_manager.get_collections()

    # Obtener la colección activa.
    def get_active_category(self):
        """
        Método encargado de retornar el nombre de la colección (entrenamiento) que se está usando
        para las consultas a la base de datos.

        Returns:
            dict: Un diccionario con el estado, mensaje y resultado de la operación.
                - 'status' (bool): Estado de la operación.
                - 'message' (str): Mensaje de éxito o error.
                - 'content' (str): El nombre del entrenamiento seleccionado.
        """
        category = self._model_manager.get_selected_category()

        if not category:
            return {'status': False, 'message': 'No se ha seleccionado un entrenamiento.'}

        return {'status': True, 'message': 'Se obtuvo el nombre del entrenamiento que se está utilizando',
                'content': category}

    # Cambiar la colección activa.
    def change_category(self, category: str):
        """
        Método para asignar una nueva colección (entrenamiento) activa para las consultas a la base de datos.

        Args:
            category (str): Nombre de la colección (entrenamiento) a utilizar.

        Returns:
            dict: Un diccionario con el estado, mensaje y resultado de la operación.
                - 'status' (bool): Estado de la operación.
                - 'message' (str): Mensaje de éxito o error.
        """
        self._model_manager.set_category(category=category)

        return {'status': True, 'message': f'Se ha seleccionado el entrenamiento: {category}'}

    # Obtener el número de coincidencias del RAG a obtener.
    def get_rag_number_matches(self):
        """
        Método encargado de retornar el número establecido de coincidencias a obtener de la base de datos vectorial.

        Returns:
            dict: Un diccionario con el estado, mensaje y resultado de la operación.
                - 'status' (bool): Estado de la operación.
                - 'message' (str): Mensaje de éxito o error.
                - 'content' (int): El número establecido de coincidencias a obtener de la base de datos vectorial.
        """

        return {'status': True,
                'message': 'Se obtuvo el número establecido de coincidencias a obtener de la base de datos vectorial.',
                'content': self._model_manager.get_k()}

    # Cambiar el número de coincidencias del RAG a obtener.
    def change_rag_number_matches(self, k: int):
        """
        Método encargado de cambiar el número establecido de coincidencias a obtener de la base de datos vectorial.

        Args:
            k (int): Número de coincidencias a obtener de la base de datos vectorial.

        Returns:
            dict: Un diccionario con el estado, mensaje y resultado de la operación.
                - 'status' (bool): Estado de la operación.
                - 'message' (str): Mensaje de éxito o error.
        """
        self._model_manager.set_k(k)

        return {'status': True,
                'message': f'Se cambió el número establecido de coincidencias a obtener de la base de datos vectorial.'}

    # Obtener el nivel de respuesta del modelo.
    def get_level_response(self):
        """
        Método encargado de retornar el nivel establecido en la calidad de respuesta del modelo.

        Returns:
             dict: Un diccionario con el estado, mensaje y resultado de la operación.
                - 'status' (bool): Estado de la operación.
                - 'message' (str): Mensaje de éxito o error.
                - 'content' (int): El nivel establecido en la calidad de respuesta del modelo.
        """

        return {'status': True, 'message': 'Se obtuvo el nivel establecido en la calidad de respuesta del modelo.',
                'content': self._model_manager.get_level()}

    # Cambiar el nivel de respuesta del modelo.
    def change_level_response(self, level: int):
        """
        Método encargado de cambiar el nivel establecido en la calidad de respuesta del modelo.

        Args:
            level (int): Nivel de la calidad de respuesta del modelo.

        Returns:
             dict: Un diccionario con el estado, mensaje y resultado de la operación.
                - 'status' (bool): Estado de la operación.
                - 'message' (str): Mensaje de éxito o error.
        """
        self._model_manager.set_level(level)

        return {'status': True,
                'message': 'Se cambió de manera correcta el nivel de la calidad de respuesta del modelo.'}

    # Crear colección
    def create_collection(self, file_content: bytes, file_extension: str, category: str):
        """
        Método encargado de crear una nueva colección (entrenamiento).

        Args:
            file_content (bytes): Contenido del documento.
            file_extension (str): Extensión del documento ingresado.
            category (str): Los metadatos (entrenamiento) que se le asignarán a los datos.

        Returns:
            dict: Un diccionario con el estado, mensaje y resultado de la operación.
                - 'status' (bool): Estado de la operación.
                - 'message' (str): Mensaje de éxito o error.
        """
        return self.db_manager.create_collection(file_content=file_content,
                                                 file_extension=file_extension,
                                                 category=category)

    # Borrar Colección
    def delete_collection(self, category: str):
        """
        Método encargado de eliminar una colección (entrenamiento).

        Args:
            category (str): Nombre de la colección (entrenamiento) a eliminar.

        Returns:
             dict: Un diccionario con el estado, mensaje y resultado de la operación.
                - 'status' (bool): Estado de la operación.
                - 'message' (str): Mensaje de éxito o error.
        """
        return self.db_manager.delete_collection(category=category)

    # Actualizar Colección
    def update_collection(self, file_content: bytes, file_extension: str, category):
        """
        Método encargado de actualizar una colección (entrenamiento).

        Args:
            file_content (bytes): Contenido del documento.
            file_extension (str): Extensión del documento ingresado.
            category (str): Los metadatos (entrenamiento) que se le asignarán a los datos.

        Returns:
             dict: Un diccionario con el estado, mensaje y resultado de la operación.
                - 'status' (bool): Estado de la operación.
                - 'message' (str): Mensaje de éxito o error.
        """
        return self.db_manager.update_collection(file_content=file_content,
                                                 file_extension=file_extension,
                                                 category=category)

    # Consultar Colección
    def query_collection(self, query: str, category: str):
        """
        Método para consultar una colección (entrenamiento).

        Args:
            query (str): Consulta realizada por el usuario.
            category (str): Colección (entrenamiento) en la que se buscará la consulta del usuario.

        Returns:
             dict: Un diccionario con el estado, mensaje y resultado de la operación.
                - 'status' (bool): Estado de la operación.
                - 'message' (str): Mensaje de éxito o error.
                - 'content' (list): Lista con los resultados de la consulta.
        """
        return self.db_manager.db_query(query=query, category=category, k=self._model_manager.get_k())

    # Validar configuración del chat
    def validate_model_settings(self):
        """
        Método encargado de validar si todas las opciones de configuración necesarias para interactuar con el chat
        están configuradas.

         Returns:
             dict: Un diccionario con el estado, mensaje y resultado de la operación.
                - 'status' (bool): Estado de la operación.
                - 'message' (str): Mensaje de éxito o error.
        """
        category = self._model_manager.get_selected_category()

        if not category:
            return {'status': False, 'message': 'No se ha seleccionado un entrenamiento.'}

        model = self._model_manager.get_selected_model()

        if not model:
            return {'status': False, 'message': 'No se ha seleccionado un modelo con el cual interactuar.'}

        return {'status': True, 'message': 'Todo está listo para iniciar el proceso de comunicación con el modelo.'}

    # Chat con el modelo de Ollama activo en stream
    def query_ollama_model(self, query: str):
        """
        Método para consultar el modelo de ollama.

        Args:
            query (str): Consulta realizada al modelo.

        Returns:
            generator: Un generador con la respuesta del modelo a la consulta.
        """

        try:

            # Recuperación de contexto relevante
            # content_chunks = self.db_manager.db_query(query,
            #                                           self._model_manager.get_selected_category(),
            #                                           self._model_manager.get_k())['content']

            # rag_response = "\n\n- ".join(chunk.strip() for chunk in content_chunks)

            rag_response = "\n\n- ".join(
                [re.sub(r'\s+', ' ', chunk.strip())
                 for chunk in self.db_manager.db_query(query,
                                                       self._model_manager.get_selected_category(),
                                                       self._model_manager.get_k())['content']])

            print(rag_response)

            #
            #
            # rag_response = "\n\n- ".join(self.db_manager.db_query(query,
            #                                                   self._model_manager.get_selected_category(),
            #                                                   self._model_manager.get_k())['content'])
            #
            # print(rag_response)
            # print(self._model_manager.get_level())

            # Definición del nivel de respuesta
            levels = ["de manera breve, directa y resumida.",
                      "sin detallar demasiado.",
                      "de manera profunda y extensa."
            ]

            level_text = levels[self._model_manager.get_level()]

            # levels = ["de manera breve, directa y resumida.",
            #           "sin detallar demasiado.",
            #           "de manera profunda y extensa."]

            # custom_query = [
            #     {'role': 'system', 'content': 'Tu nombre es Tomás, eres un asistente virtual que pertenece a '
            #                                   'Grupo Fórmula.'},
            #     {'role': 'user', 'content': f'Con base a un sistema de generación aumentada de recuperación obtendrás '
            #                                 f'información relevante para responder a la pregunta del usuario, sin '
            #                                 f'embargo, debes tomar en cuenta que no toda la información proporcionada '
            #                                 f'es relevante. La información recuperada es: \n\n{rag_response}'},
            #     {'role': 'user', 'content': f'La pregunta del usuario a la que debes responder '
            #                                 f'({levels[self._model_manager.get_level()]}) es: {query}'}
            # ]

            # Prompt para el modelo
            custom_query = [
                {'role': 'system', 'content': (
                    'Tu nombre es Tomás, eres un asistente virtual que pertenece a Grupo Fórmula. '
                    'Usarás información recuperada mediante RAG para responder de forma coherente y útil. '
                    'Ignora información irrelevante si no ayuda a responder. '
                    f'Nivel de detalle requerido: {level_text}'
                )},
                {'role': 'user', 'content': f'Información recuperada:\n\n{rag_response}'},
                {'role': 'user', 'content': f'Pregunta del usuario: {query}'}
            ]

            for item in custom_query:
                print(item)

            response = self._model_manager.ollama_instance.client.chat(model=self._model_manager.get_selected_model(),
                                                                       messages=custom_query,
                                                                       stream=True)
            for chunk in response:
                yield chunk['message']['content']

        except Exception as error:
            yield (f'Lo siento, ocurrió un problema de tipo {str(error)} al procesar tu pregunta. '
                   f'Por favor, intenta de nuevo.')

