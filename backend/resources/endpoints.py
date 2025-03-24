from flask.views import MethodView
from flask_smorest import Blueprint
from LLM.new_llm_manager import ModelManager, ChatSession
from schemas.schemas import QuerySchema
from flask import jsonify, request
from schemas.schemas import PlainQueryRag, PlainDeleteCategory, PlainQueryUser, PlainChangeModel
from RAG.DBController import RAGManager
from flask import Response

blp = Blueprint("OLLAMAController", __name__, description="Chatbot con Ollama.")

manager = ModelManager()
chat = ChatSession(manager)


@blp.route("/rag")
class Collections(MethodView):

    def get(self):
        """
        Método para obtener las categorías existentes dentro de la base de datos vectorial.
        :return: Una lista de las categorías.
        """
        categories = chat.get_categories()
        print(f">>> {chat.get_categories()}")
        return {"categories": chat.get_categories()}

    def post(self):
        """
        Método para añadir un documento a una colección o crear una nueva.
        :return: El estado de la operación (True, False).
        """
        if "file" not in request.files:
            return jsonify({"error": "No se encontró ningún archivo en la solicitud."}), 400

        file = request.files["file"]
        category = request.form.get("category")  # Obtener categoría desde el formulario

        if not category:
            return jsonify({"error": "Debes proporcionar un nombre de categoría."}), 400

        if file.filename == "":
            return jsonify({"error": "No se seleccionó ningún archivo."}), 400

        file_extension = file.filename.rsplit(".", 1)[-1].lower()
        file_content = file.read()

        result = chat.add_documents(category=category, file_content=file_content, file_extension=file_extension)

        return jsonify({"status": result})

    @blp.arguments(PlainDeleteCategory)
    def delete(self,data):
        """
        Método para eliminar una categoría.
        :param data: Categoría en formato JSON.
        :return: El estado de la operación (True, False).
        """
        category = data["category"]
        result = chat.delete_documents(category)
        return {"status": result}


@blp.route("/rag/query")
class RAGQuery(MethodView):

    @blp.arguments(PlainQueryRag)
    def post(self, data):
        """
        Método para realizar una consulta a la base de datos vectorial.
        :param data: Un JSON con los datos solicitados por el método.
        :return: Una lista con las coincidencias encontradas.
        """
        query = data["query"]
        category = data["category"]
        k = data["k"]

        result = chat.query_documents(query, category, k)
        return {"result": result}








@blp.route("/ollama")
class QueryModel(MethodView):

    def get(self):
        """
        Método para obtener el modelo activo para las consultas.
        :return: Un JSON con los datos solicitados.
        """
        return {"model": manager.selected_model}

    @blp.arguments(PlainQueryUser)  # Usamos el decorador @blp.arguments con el esquema
    def post(self, data):
        """
        Método para realizar una consulta al modelo activo.
        :param data: JSON con los datos solicitados.
        :return: La respuesta del modelo en stream.
        """
        query = data["query"]
        rag = data["rag"]
        level = data["level"]
        category = data["category"]

        print(f">>> Query: {query}\nRAG: {rag}\nLevel:{level}\nCategory:{category}")

        try:
            # Retornar la respuesta
            return Response(chat.query_model(query=query, rag=rag, level=level, category=category), content_type="text/plain")

        except Exception as e:
            # En caso de error en el modelo, respondemos con un mensaje de error
            return {"message": "Error processing request", "error": str(e)}, 500



@blp.route("/ollama/change-model")
class ChangeModel(MethodView):

    def get(self):
        """
        Método para obtener la lista de modelos disponibles.
        :return: Una lista con los elementos disponibles.
        """
        return {"models": manager.available_models}

    @blp.arguments(PlainChangeModel)
    def post(self, data):
        """
        Método para cambiar el modelo activo.
        :param data: Un JSON con los datos solicitados.
        :return: Un JSON con el estado de la operación.
        """

        index = data["index"]

        try:
            # Validación del índice (por ejemplo, verificar que sea un índice válido)
            if index < 0 or index >= len(manager.available_models):
                return jsonify({"message": "Índice de modelo fuera de rango"}), 400

            if manager.available_models[index] == manager.selected_model:
                return {"message": f"El modelo {manager.selected_model} ya se encuentra seleccionado"}, 200

            # Intentar cargar el modelo usando el índice
            manager.load_model(index)

            # Responder con éxito si el modelo se carga correctamente
            return jsonify({"message": f"Modelo cambiado a: {manager.selected_model}"}), 200

        except IndexError:
            # Si el índice no es válido o no se puede cargar el modelo
            return jsonify({"message": "Error al cargar el modelo", "error": "Índice no válido"}), 400

        except Exception as e:
            # Capturar cualquier otra excepción inesperada
            return jsonify({"message": "Error interno del servidor", "error": str(e)}), 500

