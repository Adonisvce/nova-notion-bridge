from flask import Blueprint, jsonify

command_center_bp = Blueprint('command_center', __name__)

@command_center_bp.route('/command-center/status', methods=['GET'])
def command_center_status():
    return jsonify({
        "message": "Command Center is online and operational",
        "status": "success"
    })
