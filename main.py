import os
from flask import Flask
from dotenv import load_dotenv

# Load environment variables from .env (locally)
load_dotenv()

# Import the blueprint registration function
from routes import register_all_routes

# Create the Flask app
app = Flask(__name__)

# Register all routes (blueprints)
register_all_routes(app)

# Optional: Root confirmation
@app.route("/", methods=["GET"])
def index():
    return "Nova OS is running!"

# Optional: Test route for debugging
@app.route("/test", methods=["GET"])
def test():
    return "Test route working!"

# WSGI entry point for gunicorn (Render)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))