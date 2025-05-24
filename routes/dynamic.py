# routes/dynamic.py

from flask import jsonify

def register_dynamic_routes(app):
    @app.route("/")
    def index():
        return "Nova OS is live with modular architecture!", 200
