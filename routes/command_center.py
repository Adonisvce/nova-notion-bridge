
# routes/command_center.py

from flask import jsonify

def register_command_center_routes(app):
    @app.route("/command-center", methods=["GET"])
    def command_center_status():
        return jsonify({"message": "Command Center route active."}), 200
