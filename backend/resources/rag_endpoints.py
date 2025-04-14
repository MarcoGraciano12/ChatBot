"""
Módulo que define los controladores de endpoints RESTFUL para la interacción con el sistema de
Generación Aumentada por Recuperación (RAG) usando Flask-Smorest.

Este controlador permite:
- Gestionar el modelo LLM activo.
- Consultar y cambiar la colección (entrenamiento) activa.
- Ajustar parámetros como número de documentos recuperados y nivel de respuesta.
- Listar, crear, actualizar y eliminar colecciones de entrenamiento.
- Realizar consultas tanto al sistema RAG como al modelo Ollama directamente.

Blueprint:
    - 'RAG Controller': Agrupa todas las rutas relacionadas con sistema RAG.
"""

# Importación de Módulos
from flask.views import MethodView
from flask_smorest import Blueprint
from flask import request
from transformers.models.auto.modeling_flax_auto import FLAX_MODEL_FOR_SEQ_TO_SEQ_CAUSAL_LM_MAPPING_NAMES

from schemas import rag_schema
from flask import Response
from RAGController.chat_session import ChatSession

blp = Blueprint("RAG Controller",
                __name__,
                description="Controlador del Sistema de Generación Aumentada por Recuperación")

manager = ChatSession()

# Declaración de Clases
@blp.route("/model")
class ModelManager(MethodView):
    """
    Clase que gestiona el modelo de lenguaje activo para el sistema RAG.

    Rutas:
        GET /model: Obtiene el modelo actualmente activo.
        POST /model: Cambia el modelo activo según el índice proporcionado.
    """

    def get(self):
        """
        Método que retorna al modelo que se encuentre activado.

        Returns:
            dict: Un diccionario con el estado, mensaje y resultado de la operación.
                - 'status' (bool): Estado de la operación.
                - 'message' (str): Mensaje de éxito o error.
                - 'content' (str): El nombre del modelo seleccionado.
        """
        return manager.get_active_model()

    @blp.arguments(rag_schema.PlainChangeModel)
    def post(self, data):
        """
        Método que permite cambiar el modelo activo según el usuario indique.

        Args:
            data (): JSON con los datos solicitados para realizar la operación.
                - 'index' (int): Indice del modelo en la lista de modelos disponibles.

        Returns:
            dict: Un diccionario con el estado, mensaje y resultado de la operación.
                - 'status' (bool): Estado de la operación.
                - 'message' (str): Mensaje de éxito o error.
        """

        index = data["index"]

        if index < 0:
            return {'status': False, 'message': "El indice debe ser mayor a cero."}

        return manager.change_model(index)

    @blp.arguments(rag_schema.PlainModifyModel)
    def delete(self, data):

        model = data['model']

        return manager.delete_model(llm_name=model)

    @blp.arguments(rag_schema.PlainModifyModel)
    def put(self, data):
        model = data['model']
        return Response(manager.download_model(ll_name=model), mimetype='text/event-stream')


@blp.route("/collection")
class CollectionManager(MethodView):
    """
    Clase que gestiona la colección (entrenamiento) activa usada en el sistema RAG.

    Rutas:
        GET /collection: Obtiene la colección actualmente seleccionada.
        POST /collection: Cambia la colección activa según el nombre proporcionado.
    """

    def get(self):
        """
        Método encargado de retornar el nombre de la colección (entrenamiento) que se está usando
        para las consultas a la base de datos.

        Returns:
            dict: Un diccionario con el estado, mensaje y resultado de la operación.
                - 'status' (bool): Estado de la operación.
                - 'message' (str): Mensaje de éxito o error.
                - 'content' (str): El nombre del entrenamiento seleccionado.
        """
        return manager.get_active_category()

    @blp.arguments(rag_schema.PlainChangeCategory)
    def post(self, data):
        """
        Método para asignar una nueva colección (entrenamiento) activa para las consultas a la base de datos.

        Args:
            data (): JSON con los datos solicitados para realizar la operación.
                - 'category' (str): Nombre del entrenamiento.

        Returns:
            dict: Un diccionario con el estado, mensaje y resultado de la operación.
                - 'status' (bool): Estado de la operación.
                - 'message' (str): Mensaje de éxito o error.
        """
        categories = manager.get_available_collections()

        category = data["category"]

        if category not in categories:
            return {"status": False, "message": f"El entrenamiento {category} no existe."}

        return manager.change_category(category=category)


@blp.route("/rag-k")
class MatchesKManager(MethodView):
    """
    Clase encargada de gestionar el número de coincidencias (documentos) recuperados
    desde la base de datos vectorial durante una consulta RAG.

    Rutas:
        GET /rag-k: Obtiene el número actual de coincidencias configuradas.
        POST /rag-k: Cambia el número de coincidencias a recuperar.
    """

    def get(self):
        """
        Método encargado de retornar el número establecido de coincidencias a obtener de la base de datos vectorial.

        Returns:
            dict: Un diccionario con el estado, mensaje y resultado de la operación.
                - 'status' (bool): Estado de la operación.
                - 'message' (str): Mensaje de éxito o error.
                - 'content' (int): El número establecido de coincidencias a obtener de la base de datos vectorial.
        """

        return manager.get_rag_number_matches()

    @blp.arguments(rag_schema.PlainChangeK)
    def post(self, data):
        """
        Método encargado de cambiar el número establecido de coincidencias a obtener de la base de datos vectorial.

        Args:
            data (): JSON con los datos solicitados para realizar la operación.
                - 'k' (int): El número establecido de coincidencias a obtener de la base de datos vectorial.

        Returns:
            dict: Un diccionario con el estado, mensaje y resultado de la operación.
                - 'status' (bool): Estado de la operación.
                - 'message' (str): Mensaje de éxito o error.
        """
        k = data["k"]

        return manager.change_rag_number_matches(k=k)


@blp.route("/level")
class LevelManager(MethodView):
    """
    Clase que gestiona el nivel de calidad de respuesta configurado para el modelo LLM.

    Rutas:
        GET /level: Obtiene el nivel de calidad de respuesta actual.
        POST /level: Cambia el nivel de calidad de respuesta.
    """

    def get(self):
        """
        Método encargado de retornar el nivel establecido en la calidad de respuesta del modelo.

        Returns:
             dict: Un diccionario con el estado, mensaje y resultado de la operación.
                - 'status' (bool): Estado de la operación.
                - 'message' (str): Mensaje de éxito o error.
                - 'content' (int): El nivel establecido en la calidad de respuesta del modelo.
        """

        return manager.get_level_response()

    @blp.arguments(rag_schema.PlainChangeLevel)
    def post(self, data):
        """
        Método encargado de cambiar el nivel establecido en la calidad de respuesta del modelo.

        Args:
            data (): JSON con los datos solicitados para realizar la operación.
                - 'level' (int): Nivel de la calidad de respuesta del modelo.

        Returns:
             dict: Un diccionario con el estado, mensaje y resultado de la operación.
                - 'status' (bool): Estado de la operación.
                - 'message' (str): Mensaje de éxito o error.
        """
        level = data["level"]

        return manager.change_level_response(level)


@blp.route("/models")
class ModelsManager(MethodView):
    """
    Clase que gestiona la lista de modelos disponibles de Ollama.

    Rutas:
        GET /models: Obtiene todos los modelos LLM disponibles en el entorno local.
    """

    def get(self):
        """
        Método que retorna la lista de modelos disponibles de Ollama.

        Returns:
            dict: Un diccionario con el estado, mensaje y resultado de la operación.
                - 'status' (bool): Estado de la operación.
                - 'message' (str): Mensaje de éxito o error.
                - 'content' (list): Una lista que contiene los modelos de Ollama disponibles en local.
        """

        return {'status': True, 'message': 'Se obtuvo de manera correcta la lista de modelos disponibles.',
                'content': manager.get_available_models()}


@blp.route("/collections")
class CollectionsManager(MethodView):
    """
    Clase que permite gestionar las colecciones (entrenamientos) disponibles para el sistema RAG.

    Rutas:
        GET /collections: Lista todas las colecciones disponibles.
        POST /collections: Crea una nueva colección subiendo un archivo.
        DELETE /collections: Elimina una colección existente.
        PUT /collections: Actualiza una colección existente con un nuevo archivo.
    """

    def get(self):
        """
        Método encargado de retornar la lista de entrenamientos disponibles.

        Returns:
            dict: Un diccionario con el estado, mensaje y resultado de la operación.
                - 'status' (bool): Estado de la operación.
                - 'message' (str): Mensaje de éxito o error.
                - 'content' (list): Una lista con las colecciones (entrenamientos) disponibles.

        """

        return {'status': True, 'message': 'Se obtuvo de manera correcta la lista de entrenamientos disponibles.',
                'content': manager.get_available_collections()}

    def post(self):
        """
        Método encargado de crear una nueva colección (entrenamiento).

        Returns:
             dict: Un diccionario con el estado, mensaje y resultado de la operación.
                - 'status' (bool): Estado de la operación.
                - 'message' (str): Mensaje de éxito o error.
        """

        if "file" not in request.files:
            return {"status": False, "message": "No se encontró ningún archivo en la solicitud."}

        file = request.files["file"]
        category = request.form.get("category")  # Obtener categoría desde el formulario

        if not category:
            return {"status": False, "message": "Debes proporcionar una categoría."}

        if file.filename == "":
            return {"status": False, "message": "No se seleccionó ningún archivo."}

        file_extension = file.filename.rsplit(".", 1)[-1].lower()
        file_content = file.read()

        return manager.create_collection(file_content=file_content,
                                         file_extension=file_extension,
                                         category=category)

    @blp.arguments(rag_schema.PlainChangeCategory)
    def delete(self, data):
        """
        Método encargado de eliminar una colección (entrenamiento).

        Args:
            data (JSON): Un json con los datos solicitados.
                - 'category' (str): Los metadatos (entrenamiento) que se le asignarán a los datos.

        Returns:
             dict: Un diccionario con el estado, mensaje y resultado de la operación.
                - 'status' (bool): Estado de la operación.
                - 'message' (str): Mensaje de éxito o error.
        """

        category = data["category"]

        return manager.delete_collection(category=category)

    def put(self):
        """
        Método encargado de actualizar una colección (entrenamiento).

        Returns:
             dict: Un diccionario con el estado, mensaje y resultado de la operación.
                - 'status' (bool): Estado de la operación.
                - 'message' (str): Mensaje de éxito o error.

        """

        if "file" not in request.files:
            return {"status":False, "message":"No se encontró ningún archivo en la solicitud."}

        file = request.files["file"]
        category = request.form.get("message")  # Obtener categoría desde el formulario

        if not category:
            return {"status": False, "message": "Debes proporcionar una categoría."}

        if file.filename == "":
            return {"status": False, "message": "No se seleccionó ningún archivo."}

        file_extension = file.filename.rsplit(".", 1)[-1].lower()
        file_content = file.read()

        return manager.update_collection(file_content=file_content,
                                                     file_extension=file_extension,
                                                     category=category)


@blp.route("/rag")
class RAGManager(MethodView):
    """
    Clase que permite realizar consultas al sistema RAG, especificando la colección.

    Rutas:
        GET /rag: Realiza una consulta a una colección específica del sistema RAG.
    """

    @blp.arguments(rag_schema.PlainQueryCollection)
    def get(self, data):
        """
        Método para realizar peticiones a una colección de la base de datos.
        """

        query = data["query"]
        category = data["category"]

        return manager.query_collection(query=query, category=category)


@blp.route("/ollama/chat")
class OllamaManager(MethodView):
    """
    Clase que permite interactuar directamente con un modelo Ollama, ya sea para validarlo o consultarlo.

    Rutas:
        GET /ollama/chat: Verifica que el modelo tenga la configuración adecuada.
        POST /ollama/chat: Envía un prompt directamente al modelo Ollama.
    """

    def get(self):

        return manager.validate_model_settings()

    @blp.arguments(rag_schema.PlainQueryModel)
    def post(self,data):

        query = data["query"]

        return Response(manager.query_ollama_model(query), content_type="text/plain")