
from flask import Flask, jsonify
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Import and register dynamic routes
from routes.dynamic import register_dynamic_routes
register_dynamic_routes(app)

# Import and register logic syncer
from modules.logic_syncer import logic_syncer
app.add_url_rule('/sync-logic', 'sync_logic', logic_syncer.sync_logic, methods=['POST'])

# Root route (optional fallback)
@app.route('/')
def index():
    return "Nova OS is live with modular architecture!", 200

if __name__ == '__main__':
    app.run(debug=True)
