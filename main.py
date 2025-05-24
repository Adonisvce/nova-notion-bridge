
from flask import Flask, request, jsonify, redirect
import os
import requests
from notion_client import Client
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

notion = Client(auth=os.getenv("NOTION_API_KEY"))

# In-memory registry for endpoints
endpoint_registry = {}

# OAuth Routes
@app.route("/oauth/start")
def oauth_start():
    redirect_uri = os.getenv("OAUTH_REDIRECT_URI")
    client_id = os.getenv("NOTION_CLIENT_ID")
    return redirect(f"https://api.notion.com/v1/oauth/authorize?owner=user&client_id={client_id}&redirect_uri={redirect_uri}&response_type=code")

@app.route("/oauth/callback")
def oauth_callback():
    code = request.args.get("code")
    if not code:
        return "Missing code", 400

    token_response = requests.post(
        "https://api.notion.com/v1/oauth/token",
        headers={"Content-Type": "application/json"},
        json={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": os.getenv("OAUTH_REDIRECT_URI")
        },
        auth=(os.getenv("NOTION_CLIENT_ID"), os.getenv("NOTION_CLIENT_SECRET"))
    )

    return jsonify(token_response.json())

# Sync Logic from Notion
@app.route("/sync-logic", methods=["POST"])
def sync_logic():
    try:
        logic_db_id = os.getenv("NOTION_LOGIC_CONFIG_DB_ID")
        if not logic_db_id:
            return jsonify({"error": "Missing NOTION_LOGIC_CONFIG_DB_ID"}), 400

        entries = notion.databases.query(database_id=logic_db_id)["results"]
        global endpoint_registry
        endpoint_registry.clear()

        for entry in entries:
            props = entry["properties"]
            if not props["Enabled"]["checkbox"]:
                continue

            route = props["Path"]["rich_text"][0]["plain_text"]
            operation_id = props["Operation ID"]["rich_text"][0]["plain_text"]
            logic_code = props["Logic"]["rich_text"][0]["plain_text"]

            def generate_handler(logic):
                def handler():
                    try:
                        local_vars = {"request": request}
                        exec(logic, {}, local_vars)
                        return jsonify(local_vars.get("response", {"message": "No response defined"}))
                    except Exception as e:
                        return jsonify({"error": str(e)}), 500
                return handler

            endpoint_registry[route] = generate_handler(logic_code)
            app.add_url_rule(route, operation_id, endpoint_registry[route], methods=["POST"])

        return jsonify({"status": "Logic synced successfully", "routes": list(endpoint_registry.keys())})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Default Root Route
@app.route("/", methods=["GET"])
def index():
    return jsonify({"message": "Nova Notion Bridge is live!"})
