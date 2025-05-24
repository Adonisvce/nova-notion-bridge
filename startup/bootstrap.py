
# startup/bootstrap.py

from database.notion_client import NotionClient
from modules.logic_engine.executor import LogicExecutor
from routes import register_routes

notion = None
executor = None

def bootstrap(app):
    global notion, executor

    # Initialize Notion client
    notion = NotionClient(token=app.config.get("NOTION_TOKEN"))

    # Initialize Logic Executor
    executor = LogicExecutor()

    # Register all route groups
    register_routes(app)

    print("✅ Bootstrap complete. System is ready.")
