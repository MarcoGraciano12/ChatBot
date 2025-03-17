from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from pyexpat.errors import messages
from schemas.test_schema import PlainTestSchema

blp = Blueprint("Test", __name__, description="Esto es una prueba.")

@blp.route("/test/<string:name>")
class Test(MethodView):
    @blp.response(200,PlainTestSchema)
    def get(self, name):
        try:
            return {"name": f"¡¡La prueba fue exitosa {name}!!"}
        except KeyError:
            abort(404, message="Ocurrió un error con la función de prueba.")