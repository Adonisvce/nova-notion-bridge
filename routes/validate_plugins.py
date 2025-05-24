from flask import Blueprint, jsonify

validate_bp = Blueprint("validate", __name__, url_prefix="/validate")

@validate_bp.route("/", methods=["GET"])
def validate_plugins():
    return jsonify({"status": "Plugin validation active"})

