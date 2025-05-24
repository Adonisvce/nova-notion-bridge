from flask import Blueprint

command_center_bp = Blueprint("command_center", __name__)

@command_center_bp.route("/command-center", methods=["GET"])
def command_center():
    return "Command Center Endpoint Loaded"
