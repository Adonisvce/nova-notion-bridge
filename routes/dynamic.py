from flask import Blueprint, jsonify

dynamic_bp = Blueprint("dynamic", __name__, url_prefix="/dynamic")

@dynamic_bp.route("/", methods=["GET"])
def dynamic_status():
    return jsonify({"status": "Dynamic routes are active"})

