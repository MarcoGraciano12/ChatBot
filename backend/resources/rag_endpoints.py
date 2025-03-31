from flask.views import MethodView
from flask_smorest import Blueprint

from flask import request
from schemas import rag_schema
from flask import Response
from RAGController.chat_session import ChatSession

blp = Blueprint("RAG Controller",
                __name__,
                description="Controlador del Sistema de Generación Aumentada por Recuperación")

manager = ChatSession()


@blp.route("/model")
class ModelManager(MethodView):

    def get(self):
        """
        Método para obtener el modelo activo.
        """

        # Se obtiene el modelo activo asignado.
        status, response = manager.get_active_model()

        return {"status":status, "response":response}

    @blp.arguments(rag_schema.PlainChangeModel)
    def post(self, data):

        index = data["index"]

        if index < 1:
            return {"status":False, "response":"El indice debe ser mayor a 0."}

        status, response = manager.change_model(index)

        return {"status": status, "response": response}


@blp.route("/collection")
class CollectionManager(MethodView):

    def get(self):
        status, response = manager.get_active_category()

        return {"status": status, "response": response}

    @blp.arguments(rag_schema.PlainChangeCategory)
    def post(self, data):

        categories = manager.get_available_collections()

        category = data["category"]

        if category not in categories:
            return {"status": False, "response": f"El entrenamiento {category} no existe."}

        status, response = manager.change_category(category=category)

        return {"status": status, "response": response}


@blp.route("/rag-k")
class DocumentesRecovered(MethodView):

    def get(self):
        status, response = manager.get_rag_number_matches()

        return {"status": status, "response": response}

    @blp.arguments(rag_schema.PlainChangeK)
    def post(self, data):
        k = data["k"]

        status, response = manager.change_rag_number_matches(k=k)

        return {"status": status, "response": response}


@blp.route("/level")
class DocumentesRecovered(MethodView):

    def get(self):
        status, response = manager.get_level_response()

        return {"status": status, "response": response}

    @blp.arguments(rag_schema.PlainChangeLevel)
    def post(self, data):
        level = data["level"]

        status, response = manager.change_level_response(level)

        return {"status": status, "response": response}


@blp.route("/models")
class ModelsManager(MethodView):

    def get(self):
        response = manager.get_available_models()
        return {"status":True, "response":response}


@blp.route("/collections")
class CollectionsManager(MethodView):

    def get(self):
        response = manager.get_available_collections()
        return {"status":True, "response":response}

    def post(self):

        if "file" not in request.files:
            return {"status": False, "response": "No se encontró ningún archivo en la solicitud."}

        file = request.files["file"]
        category = request.form.get("category")  # Obtener categoría desde el formulario

        if not category:
            return {"status": False, "response": "Debes proporcionar una categoría."}

        if file.filename == "":
            return {"status": False, "response": "No se seleccionó ningún archivo."}

        file_extension = file.filename.rsplit(".", 1)[-1].lower()
        file_content = file.read()

        status, response = manager.create_collection(file_content=file_content,
                                                     file_extension=file_extension,
                                                     category=category)

        return {"status":status, "response":response}

    @blp.arguments(rag_schema.PlainChangeCategory)
    def delete(self, data):

        category = data["category"]

        status, response = manager.delete_collection(category=category)

        return {"status": status, "response": response}

    def put(self):

        if "file" not in request.files:
            return {"status":False, "response":"No se encontró ningún archivo en la solicitud."}

        file = request.files["file"]
        category = request.form.get("category")  # Obtener categoría desde el formulario

        if not category:
            return {"status": False, "response": "Debes proporcionar una categoría."}

        if file.filename == "":
            return {"status": False, "response": "No se seleccionó ningún archivo."}

        file_extension = file.filename.rsplit(".", 1)[-1].lower()
        file_content = file.read()

        status, response = manager.update_collection(file_content=file_content,
                                                     file_extension=file_extension,
                                                     category=category)

        return {"status": status, "response": response}


@blp.route("/rag")
class RAGManager(MethodView):

    @blp.arguments(rag_schema.PlainQueryCollection)
    def get(self, data):
        """
        Método para realizar peticiones a una colección de la base de datos.
        """

        query = data["query"]
        category = data["category"]

        status, response= manager.query_collection(query=query, category=category)

        return {"status": status, "response": response}


@blp.route("/ollama/chat")
class OllamaManager(MethodView):
    def get(self):
        status, response = manager.validate_model_settings()

        return {"status": status, "response": response}

    @blp.arguments(rag_schema.PlainQueryModel)
    def post(self,data):

        query = data["query"]

        return Response(manager.query_ollama_model(query), content_type="text/plain")