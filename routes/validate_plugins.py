from flask import Blueprint, jsonify
from logic_engine.executor import LogicExecutor

validate_plugins_bp = Blueprint('validate_plugins', __name__)

@validate_plugins_bp.route('/validate-plugins', methods=['POST'])
def validate_plugins():
    executor = LogicExecutor()
    loaded_plugins = list(executor.plugins.keys())
    return jsonify({
        "message": "Plugin validation complete.",
        "loaded_plugins": loaded_plugins,
        "plugin_count": len(loaded_plugins)
    })
