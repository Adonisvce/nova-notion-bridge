from flask import Blueprint, jsonify

logic_sync_bp = Blueprint("sync_logic", __name__, url_prefix="/sync-logic")

@logic_sync_bp.route("/", methods=["GET"])
def index():
    return jsonify({"status": "sync_logic route active"})
