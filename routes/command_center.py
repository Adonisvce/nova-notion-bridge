from flask import Blueprint

command_center_bp = Blueprint("command_center", __name__, url_prefix="/command-center")

# Example route
@command_center_bp.route("/", methods=["GET"])
def get_status():
    return {"status": "Command Center online"}
