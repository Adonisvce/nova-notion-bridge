import os
from flask import Flask
from dotenv import load_dotenv
from startup.auto_sync import schedule_auto_sync
from routes import register_all_routes

# Load environment variables from .env
load_dotenv()

# Start scheduled auto-sync of Notion logic
schedule_auto_sync()

# Create the Flask app
app = Flask(__name__)

# Register all blueprint routes
register_all_routes(app)

# Optional root route for health checks
@app.route("/", methods=["GET"])
def index():
    return "Nova OS is running!"

# Optional test route
@app.route("/test", methods=["GET"])
def test():
    return "Test route working!"

# WSGI entry point for gunicorn (Render)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
