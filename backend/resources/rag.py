from flask.views import MethodView
from flask_smorest import Blueprint
from schemas.schemas import QuerySchema
from RAG.manager import RAGDataHandler
from flask import jsonify

blp = Blueprint("RAG", __name__, description="Base de datos vectorial.")
rag_handler = RAGDataHandler()

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
