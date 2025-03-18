from flask import Flask
from flask_smorest import Api
from resources.test import blp as TestBlueprint
from resources.rag import blp as RagBlueprint
from resources.rag import queso as Queso
from resources.ollama_models import blp as OllamaBluePrint
from resources.chatbot_manager import blp as ChatBotBluePrint
from flask_cors import CORS  # Importamos CORS

app = Flask(__name__)

CORS(app)

app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["API_TITLE"] = "TEST REST API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

api = Api(app)

api.register_blueprint(RagBlueprint)
# api.register_blueprint(Queso)
# api.register_blueprint(OllamaBluePrint)
api.register_blueprint(ChatBotBluePrint)