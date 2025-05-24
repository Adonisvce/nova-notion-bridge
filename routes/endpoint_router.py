from flask import Blueprint

endpoint_router_bp = Blueprint("endpoint_router", __name__)

@endpoint_router_bp.route("/endpoints", methods=["GET"])
def endpoints():
    return "Endpoint Router Loaded"
