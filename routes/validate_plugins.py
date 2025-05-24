from flask import Blueprint, jsonify, request

validate_bp = Blueprint('validate_plugins', __name__)

@validate_bp.route('/validate-plugin', methods=['POST'])
def validate_plugin():
    data = request.get_json()
    plugin_name = data.get("plugin_name")
    
    if not plugin_name:
        return jsonify({"status": "error", "message": "Missing plugin_name"}), 400
    
    # Placeholder for real validation logic
    return jsonify({"status": "success", "message": f"Plugin '{plugin_name}' validated successfully."})
