from flask.views import MethodView
from flask_smorest import Blueprint

from schemas.schemas import QuerySchema
from flask import jsonify, request
from schemas.schemas import PlainQueryRag, PlainDeleteCategory
from RAG.DBController import RAGManager

blp = Blueprint("RAGController", __name__, description="Base de datos vectorial.")
rag_manager = RAGManager()


@blp.route("/rag")
class Collections(MethodView):

    def get(self):
        print(rag_manager.get_categories())
        return {"category": rag_manager.get_categories()}

    def post(self):
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

        result = rag_manager.add_documents(category=category, file_content=file_content, file_extension=file_extension)

        return jsonify({"status": result})

    @blp.arguments(PlainDeleteCategory)
    def delete(self,data):
        category = data["category"]
        result = rag_manager.delete_documents(category)
        return {"status": result}


@blp.route("/rag/query")
class RAGQuery(MethodView):
    def get(self):
        return {"Request": "Hola"}

    @blp.arguments(PlainQueryRag)
    def post(self, data):
        query = data["query"]
        category = data["category"]
        k = data["k"]

        result = rag_manager.query_documents(query, category, k)
        return {"result": result}
