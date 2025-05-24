from flask import Blueprint

dynamic_bp = Blueprint("dynamic", __name__)

@dynamic_bp.route("/dynamic", methods=["GET"])
def dynamic_route():
    return "Dynamic Route Loaded"
