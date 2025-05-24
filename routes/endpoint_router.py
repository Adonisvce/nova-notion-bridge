from flask import Blueprint, request, jsonify

endpoint_router_bp = Blueprint("endpoint_router", __name__, url_prefix="/endpoints")

@endpoint_router_bp.route("/", methods=["GET"])
def status():
    return jsonify({"status": "Endpoint Router is live"})

