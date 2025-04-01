from RAGController.model_manager import ModelManager
from RAGController.chroma_db_manager import ChromaDBManager


class ChatSession:
    """Maneja la interacción con el modelo seleccionado."""

    def __init__(self):
        self._model_manager = ModelManager()
        self.db_manager = ChromaDBManager()

    # Obtener lista de modelos disponibles.
    def get_available_models(self):
        """
        Método que retornar la lista de modelos disponibles de Ollama.
        """
        return self._model_manager.get_list_models()

    # Obtener el modelo activo.
    def get_active_model(self):
        """
        Método que retorna al modelo que se encuentre activado.
        """
        model = self._model_manager.get_selected_model()

        if not model:
            return False, "No se ha seleccionado un modelo."

        return True, model

    # Cambiar Modelo
    def change_model(self, index: int):
        """
        Método que permite cambiar el modelo activo según el usuario indique.
        """
        return self._model_manager.change_selected_model(index)

    # Obtener lista de colecciones disponibles.
    def get_available_collections(self):
        """
        Método encargado de retornar la lista de colecciones disponibles en la base de datos.
        """
        return self.db_manager.get_collections()

    # Obtener la colección activa.
    def get_active_category(self):
        category = self._model_manager.get_selected_category()

        if not category:
            return False, "No se ha seleccionado un entrenamiento."

        return True, category

    # Cambiar la colección activa.
    def change_category(self, category: str):
        """
        Método para asignar una nueva colección activa.
        """
        self._model_manager.set_category(category=category)
        return True, f"Se ha seleccionado el entrenamiento {category}."

    # Obtener el número de coincidencias del RAG a obtener.
    def get_rag_number_matches(self):
        return True, self._model_manager.get_k()

    # Cambiar el número de coincidencias del RAG a obtener.
    def change_rag_number_matches(self, k: int):
        self._model_manager.set_k(k)
        return True, f"Se cambió el número de coincidencias del RAG a {k}."

    # Obtener el nivel de respuesta del modelo.
    def get_level_response(self):
        return True, self._model_manager.get_level()

    # Cambiar el nivel de respuesta del modelo.
    def change_level_response(self, level: int):
        self._model_manager.set_level(level)
        return True, f"Se cambió el nivel de respuesta del modelo."

    # Crear colección
    def create_collection(self, file_content: bytes, file_extension: str, category):
        """
        Método que permite la creación de una nueva colección (entrenamiento) en la base de datos.
        """
        return self.db_manager.create_collection(file_content=file_content,
                                                 file_extension=file_extension,
                                                 category=category)

    # Borrar Colección
    def delete_collection(self, category):
        """
        Método que permite eliminar una colección (entrenamiento) de la base de datos.
        """
        return self.db_manager.delete_collection(category=category)

    # Actualizar Colección
    def update_collection(self, file_content: bytes, file_extension: str, category):
        """
        Método que permite actualizar una colección (entrenamiento) de la base de datos.
        """
        return self.db_manager.update_collection(file_content=file_content,
                                                 file_extension=file_extension,
                                                 category=category)

    # Consultar Colección
    def query_collection(self, query, category):
        """
        Método para consultar una colección (entrenamiento) de la base de datos.
        """
        return self.db_manager.db_query(query=query, category=category, k=self._model_manager.get_k())

    # Validar configuración del chat
    def validate_model_settings(self):
        """
        Método encargado de validar si todas las opciones de configuración necesarias para interactuar con el chat
        están configuradas.
        """
        category = self._model_manager.get_selected_category()

        if not category:
            return False, "No se ha seleccionado un entrenamiento."

        model = self._model_manager.get_selected_model()

        if not model:
            return False, "No se ha seleccionado uno modelo de llm."

        return True, "Todo está listo para consultar el llm."

    # Chat con el modelo de Ollama activo en stream
    def query_ollama_model(self, query):
        """
        Método para consultar el modelo de ollama.
        """

        rag_response = "\n".join(self.db_manager.db_query(query, self._model_manager.get_selected_category(),
                                                            self._model_manager.get_k())[1])

        print(rag_response)
        print(self._model_manager.get_level())

        try:

            levels = ["Responde de manera breve y directa.",
                      "Responde de manera normal y sin detallar demasiado.",
                      "Responde de manera profunda y extensa."]

            response = self._model_manager.ollama_instance.client.chat(
                model=self._model_manager.get_selected_model(),
                messages=[
                    {'role': 'system',
                     'content': f'Eres un asistente virtual de Grupo Fórmula. {levels[self._model_manager.get_level()]}'},
                    {'role': 'user', 'content': f"""
Con base a un sistema de generación aumentada de recuperación obtendrás información relevante para responder a la pregunta,
sin embargo, debes tomar en cuenta que no toda la información proporcionada es relevante:

{rag_response}"""},
                    {'role': 'user', 'content': query}

                ],
                stream=True
            )
            for chunk in response:
                yield chunk['message']['content']
        except Exception as e:
            print(f"❌ Error al consultar el modelo: {e}")
