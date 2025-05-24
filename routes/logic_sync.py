# routes/logic_sync.py
from flask import Blueprint, request, jsonify
import os
import requests
from utils.notion import get_database_items
from utils.codegen import generate_logic_file

logic_sync_bp = Blueprint("logic_sync", __name__)

@logic_sync_bp.route("/sync-logic", methods=["POST"])
def sync_logic():
    notion_db_id = os.getenv("NOTION_LOGIC_CONFIG_DB_ID")
    if not notion_db_id:
        return jsonify({"error": "NOTION_LOGIC_CONFIG_DB_ID not set"}), 500

    try:
        items = get_database_items(notion_db_id)
        created = []
        skipped = []
        errors = []

        for item in items:
            try:
                logic_name = item.get("Name") or item.get("name")
                logic_code = item.get("Code") or item.get("code")

                if not logic_name or not logic_code:
                    skipped.append(logic_name or "<unnamed>")
                    continue

                file_created = generate_logic_file(logic_name, logic_code)
                if file_created:
                    created.append(logic_name)
                else:
                    skipped.append(logic_name)
            except Exception as e:
                errors.append(str(e))

        return jsonify({
            "status": "complete",
            "created": created,
            "skipped": skipped,
            "errors": errors
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
