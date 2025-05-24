
from flask import Flask
from logic_engine.executor import LogicExecutor
from routes.dynamic import register_dynamic_routes
from database.notion_client import NotionClient
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# Initialize Notion client and logic executor
notion = NotionClient()
executor = LogicExecutor(notion)

# Register dynamic routes
register_dynamic_routes(app, notion, executor)

@app.route("/")
def index():
    return "Nova OS is live with modular architecture!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
