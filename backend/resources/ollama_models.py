from flask import request, Response
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from pyexpat.errors import messages
from schemas.test_schema import PlainTestSchema
from schemas.schemas import PlainQueyOllama
from RAG.manager import RAGDataHandler
from flask import jsonify
from LLM.model import OllamaChatManager


blp = Blueprint("OLLAMA", __name__, description="Large Language Model.")
# Instanciar el controlador de los LLM de Ollama
chat_manager = OllamaChatManager()
# Incializar un LLM por defecto
chat_manager.load_model_chat(0)


@blp.route("/ollama/chat")
class QueryModel(MethodView):
    @blp.arguments(PlainQueyOllama)
    def post(self, query_data):
        """
               Realiza una consulta a la base de datos RAG y devuelve los resultados.
               """
        query = query_data["query"]

        return Response(chat_manager.query_model(query), content_type="text/plain")


