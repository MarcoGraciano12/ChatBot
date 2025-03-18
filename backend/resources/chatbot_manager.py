from flask import request, Response
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from pyexpat.errors import messages
from schemas.test_schema import PlainTestSchema
from schemas.schemas import PlainQueryUser, PlainChangeModel
from RAG.manager import RAGDataHandler
from flask import jsonify
from LLM.model import OllamaChatManager
from LLM.llm_manager import ModelManager, ChatSession


blp = Blueprint("CHATBOT", __name__, description="Large Language Model.")

# Cargar el controlador de modelos
manager = ModelManager()
# Cargar el controlador del chatbot
chat = ChatSession(manager)

@blp.route("/ollama")
class QueryModel(MethodView):

    def get(self):
        return {"model": manager.selected_model}

    @blp.arguments(PlainQueryUser)  # Usamos el decorador @blp.arguments con el esquema
    def post(self, data):
        """
        Realiza una consulta a la base de datos RAG y devuelve los resultados.
        """
        query = data["query"]
        rag = data["rag"]
        level = data["level"]

        # Ahora, ya tenemos `query`, `rag`, y `level` con los valores correctos

        try:
            # Retornar la respuesta
            return Response(chat.query_model(query, rag=rag, level=level), content_type="text/plain")

        except Exception as e:
            # En caso de error en el modelo, respondemos con un mensaje de error
            return {"message": "Error processing request", "error": str(e)}, 500



@blp.route("/ollama/change-model")
class ChangeModel(MethodView):

    def get(self):
        return {"models": manager.available_models}

    @blp.arguments(PlainChangeModel)
    def post(self, data):

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

