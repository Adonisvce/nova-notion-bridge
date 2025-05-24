import os
import requests
from flask import Flask, request, jsonify, redirect
from notion_client import Client
from dotenv import load_dotenv

load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
REFLECTION_DB_ID = os.getenv("NOTION_REFLECTION_DB_ID")
LOGIC_CONFIG_DB_ID = os.getenv("NOTION_LOGIC_CONFIG_DB_ID")
COMMAND_CENTER_DB_ID = os.getenv("NOTION_COMMAND_CENTER_DB_ID")
OAUTH_CLIENT_ID = os.getenv("NOTION_CLIENT_ID")
OAUTH_CLIENT_SECRET = os.getenv("NOTION_CLIENT_SECRET")
OAUTH_REDIRECT_URI = os.getenv("OAUTH_REDIRECT_URI")

notion = Client(auth=NOTION_TOKEN)

app = Flask(__name__)

@app.route("/")
def index():
    return "Nova Notion Bridge is running."

@app.route("/oauth/start")
def oauth_start():
    auth_url = (
        f"https://api.notion.com/v1/oauth/authorize"
        f"?owner=user"
        f"&client_id={OAUTH_CLIENT_ID}"
        f"&redirect_uri={OAUTH_REDIRECT_URI}"
        f"&response_type=code"
    )
    return redirect(auth_url)

@app.route("/auth/callback")
def oauth_callback():
    code = request.args.get("code")
    if not code:
        return jsonify({"error": "Missing code in callback"}), 400

    token_response = requests.post(
        "https://api.notion.com/v1/oauth/token",
        auth=(OAUTH_CLIENT_ID, OAUTH_CLIENT_SECRET),
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": OAUTH_REDIRECT_URI,
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    token_json = token_response.json()
    access_token = token_json.get("access_token")

    if not access_token:
        return jsonify({"error": "Token exchange failed", "details": token_json}), 400

    global notion
    notion = Client(auth=access_token)
    return jsonify({"message": "Authorization complete", "token": token_json})

@app.route("/sync-logic", methods=["POST"])
def sync_logic():
    try:
        response = notion.databases.query(
            **{
                "database_id": LOGIC_CONFIG_DB_ID,
                "filter": {"property": "Status", "status": {"equals": "Live"}},
            }
        )

        logic_entries = response.get("results", [])
        logic_summary = [
            {
                "name": entry["properties"]["Name"]["title"][0]["text"]["content"] if entry["properties"]["Name"]["title"] else None,
                "type": entry["properties"].get("Type", {}).get("select", {}).get("name"),
                "status": entry["properties"].get("Status", {}).get("status", {}).get("name"),
            }
            for entry in logic_entries
        ]

        return jsonify({"message": "Logic sync complete", "entries": logic_summary})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
