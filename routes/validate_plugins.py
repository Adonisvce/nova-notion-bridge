from flask import Blueprint

validate_bp = Blueprint("validate_plugins", __name__)

@validate_bp.route("/validate-plugins", methods=["GET"])
def validate_plugins():
    return "Validate Plugins Route Loaded"
