# routes/endpoint_router.py

from flask import jsonify

def register_endpoint_routes(app):
    @app.route("/test-endpoint", methods=["GET"])
    def test_endpoint():
        return jsonify({"message": "Endpoint routing is working."}), 200
