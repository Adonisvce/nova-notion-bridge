import os
import json
from flask import Flask, request, jsonify, redirect
from notion_client import Client
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

notion = Client(auth=os.getenv("NOTION_CLIENT_SECRET"))

NOTION_CLIENT_ID = os.getenv("NOTION_CLIENT_ID")
NOTION_CLIENT_SECRET = os.getenv("NOTION_CLIENT_SECRET")
NOTION_REDIRECT_URI = os.getenv("NOTION_REDIRECT_URI")

COMMAND_CENTER_ID = os.getenv("NOTION_COMMAND_CENTER_ID")
LOGIC_CONFIG_DB_ID = os.getenv("NOTION_LOGIC_CONFIG_DB_ID")
REFLECTION_DB_ID = os.getenv("NOTION_REFLECTION_DB_ID")


@app.route("/")
def index():
    return "Nova Notion Bridge is running."


@app.route("/oauth/start")
def oauth_start():
    client_id = NOTION_CLIENT_ID
    redirect_uri = NOTION_REDIRECT_URI
    response_type = "code"
    owner = "user"
    auth_url = (
        f"https://api.notion.com/v1/oauth/authorize"
        f"?client_id={client_id}"
        f"&redirect_uri={redirect_uri}"
        f"&response_type={response_type}"
        f"&owner={owner}"
    )
    return redirect(auth_url)


@app.route("/auth/callback")
def auth_callback():
    code = request.args.get("code")
    if not code:
        return jsonify({"error": "Missing authorization code"}), 400
    return jsonify({"message": "OAuth flow complete", "code": code})


@app.route("/sync-logic", methods=["POST"])
def sync_logic():
    try:
        results = notion.databases.query(database_id=LOGIC_CONFIG_DB_ID)
        return jsonify({"message": "Logic synced successfully", "results": results})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/log-reflection", methods=["POST"])
def log_reflection():
    data = request.json
    try:
        new_page = {
            "parent": {"database_id": REFLECTION_DB_ID},
            "properties": {
                "entry": {"title": [{"text": {"content": data.get("entry", "")}}]},
                "mood": {"select": {"name": data.get("mood", "Neutral")}},
                "tags": {"multi_select": [{"name": tag} for tag in data.get("tags", [])]},
            },
        }
        response = notion.pages.create(**new_page)
        return jsonify({"message": "Reflection logged", "page": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/command-center", methods=["GET"])
def get_command_center():
    try:
        results = notion.databases.query(database_id=COMMAND_CENTER_ID)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
