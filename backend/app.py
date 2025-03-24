from flask import Flask
from flask_smorest import Api
from resources.RAGController import blp as RAGBlueprint
# from resources.chatbot_manager import blp as ChatBotBluePrint
from resources.endpoints import blp as ChatMagener
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

# api.register_blueprint(RAGBlueprint)
# api.register_blueprint(ChatBotBluePrint)
api.register_blueprint(ChatMagener)