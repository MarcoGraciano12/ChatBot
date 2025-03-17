from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from pyexpat.errors import messages
from schemas.test_schema import PlainTestSchema
from schemas.schemas import QuerySchema
from RAG.manager import RAGDataHandler
from flask import jsonify

import time
from flask import Response

blp = Blueprint("RAG", __name__, description="Base de datos vectorial.")
rag_handler = RAGDataHandler()

queso = Blueprint("chat", __name__, description="Streaming en tiempo real")

@blp.route("/rag/query")
class QueryResource(MethodView):

    @blp.arguments(QuerySchema)  # Validar los datos de entrada
    def post(self, query_data):
        """
               Realiza una consulta a la base de datos RAG y devuelve los resultados.
               """
        query = query_data["query"]
        k = query_data["k"]

        results = rag_handler.query_db(query, k)
        print(results)
        return jsonify({"query": query, "results": results})


def generar_mensaje():
    mensajes = ["Hola,", " bienvenido", " al", " chat", " de", " streaming."]
    for msg in mensajes:
        yield msg + " "  # Envía cada palabra poco a poco
        time.sleep(0.5)  # Simula un retraso en la respuesta

@queso.route("/chat/stream")
class ChatStream(MethodView):
    def get(self):
        """Retorna una respuesta en streaming"""
        return Response(generar_mensaje(), content_type="text/plain")