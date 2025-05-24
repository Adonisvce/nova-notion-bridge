from flask import Blueprint, jsonify

echo_bp = Blueprint("echo", __name__, url_prefix="/echo")

@echo_bp.route("/", methods=["GET"])
def index():
    return jsonify({"status": "echo route active"})
