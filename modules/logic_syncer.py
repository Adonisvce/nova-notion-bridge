
# modules/logic_syncer.py

from flask import jsonify
from database.notion_client import NotionClient

def logic_syncer(app, notion: NotionClient):
    @app.route("/sync-logic", methods=["POST"])
    def sync_logic():
        try:
            notion.sync_logic_routes()
            return jsonify({"message": "Logic synced."}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
