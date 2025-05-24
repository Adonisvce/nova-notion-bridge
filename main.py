from flask import Flask
from logic_engine.executor import LogicExecutor
from database.notion_client import NotionClient
from routes.dynamic import register_dynamic_routes
from routes.endpoint_router import register_endpoint_routes
from routes.command_center import register_command_center_routes
from routes.idea_inbox import register_idea_routes
from modules.logic_syncer import logic_syncer

app = Flask(__name__)
notion = NotionClient(token=None)  # Replace with actual token management
executor = LogicExecutor(notion)

register_dynamic_routes(app)
register_endpoint_routes(app, executor)
register_command_center_routes(app, notion)
register_idea_routes(app, notion)

app.add_url_rule('/sync-logic', 'sync_logic', logic_syncer, methods=['POST'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)