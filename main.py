
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

from database.notion_client import NotionClient
from logic_engine.executor import execute_logic
from logic_engine.plugins import plugin_registry
from logic_engine.plugins.builtin.echo_plugin import EchoPlugin

from routes import register_all_routes

# Create Flask app
app = Flask(__name__)

# Initialize Notion client
notion_token = os.getenv("NOTION_TOKEN")
notion = NotionClient(token=notion_token)

# Register dynamic and system routes
register_all_routes(app, notion)

# Register plugins
plugin_registry.register("echo", EchoPlugin())

# Define logic execution route
@app.route('/execute-logic', methods=['POST'])
def handle_logic_execution():
    payload = request.get_json()
    result = execute_logic(payload)
    return jsonify(result), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
