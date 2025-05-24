from flask import Blueprint, jsonify
from logic.logic_syncer import sync_logic_routes

logic_sync_bp = Blueprint("logic_sync", __name__)

@logic_sync_bp.route("/sync-logic", methods=["POST"])
def sync_logic():
    sync_logic_routes()
    return jsonify({"status": "success", "message": "Logic synced successfully"})
