from flask import Flask, request, jsonify, redirect
import os
import requests
import logging
from datetime import datetime, timezone
import json

# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = Flask(__name__)

# --- Config ---
NOTION_CLIENT_ID = os.getenv("NOTION_CLIENT_ID")
NOTION_CLIENT_SECRET = os.getenv("NOTION_CLIENT_SECRET")
NOTION_DB_ID = os.getenv("NOTION_DB_ID")
LOGIC_CONFIG_DB_ID = os.getenv("LOGIC_CONFIG_DB_ID")
REFLECTION_DB_ID = os.getenv("REFLECTION_DB_ID")
REDIRECT_URI = "https://nova-notion-bridge.onrender.com/auth/callback"
TOKEN_FILE = "token.json"

# --- Token Persistence ---
def save_token(token_dict):
    with open(TOKEN_FILE, "w") as f:
        json.dump(token_dict, f)

def load_token():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as f:
            return json.load(f)
    return {}

def get_headers():
    token_data = load_token()
    access_token = token_data.get("access_token")
    return {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }

# --- Routes ---
@app.route("/status", methods=["GET"])
def status():
    return jsonify({"status": "ok"}), 200

@app.route("/")
def home():
    return "✅ Nova Notion Bridge is live."

@app.route("/auth/start")
def auth_start():
    url = (
        f"https://api.notion.com/v1/oauth/authorize"
        f"?client_id={NOTION_CLIENT_ID}"
        f"&response_type=code"
        f"&owner=user"
        f"&redirect_uri={REDIRECT_URI}"
    )
    return redirect(url)

@app.route("/auth/callback")
def auth_callback():
    code = request.args.get("code")
    if not code:
        return "Missing authorization code", 400

    response = requests.post(
        "https://api.notion.com/v1/oauth/token",
        json={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI
        },
        auth=(NOTION_CLIENT_ID, NOTION_CLIENT_SECRET),
        headers={"Content-Type": "application/json"}
    )

    if response.status_code != 200:
        logging.error(f"OAuth failed: {response.text}")
        return jsonify({"error": "OAuth token exchange failed", "details": response.text}), 400

    token_data = response.json()
    save_token(token_data)
    logging.info("✅ OAuth token saved.")
    return jsonify({"message": "Authorization complete", "token": token_data})

@app.route("/auth/token", methods=["GET"])
def get_token():
    return jsonify(load_token())

@app.route("/sync-logic", methods=["POST"])
def sync_logic():
    try:
        notion_data = requests.post(
            "https://api.notion.com/v1/databases/{}/query".format(LOGIC_CONFIG_DB_ID),
            headers=get_headers()
        )
        if not notion_data.ok:
            return jsonify({"error": "Failed to fetch logic config", "details": notion_data.text}), 400

        logic_entries = notion_data.json().get("results", [])
        routes = []

        for entry in logic_entries:
            props = entry["properties"]
            if props.get("Published", {}).get("checkbox", False):
                logic_name = props.get("Logic Name", {}).get("title", [{}])[0].get("text", {}).get("content", "")
                endpoint = props.get("Endpoint", {}).get("url", "")
                fields = props.get("Fields", {}).get("rich_text", [{}])[0].get("text", {}).get("content", "{}")
                try:
                    fields_json = json.loads(fields)
                except:
                    fields_json = {}

                routes.append({
                    "logic_name": logic_name,
                    "endpoint": endpoint,
                    "fields": fields_json
                })

        with open("logic_registry.json", "w") as f:
            json.dump(routes, f, indent=2)

        return jsonify({"message": "Logic config synced", "routes": routes}), 200
    except Exception as e:
        logging.exception("Unexpected error in /sync-logic")
        return jsonify({"error": "Internal server error"}), 500

@app.route("/run-logic", methods=["POST"])
def run_logic():
    try:
        logic_request = request.get_json()
        logic_name = logic_request.get("logic_name")
        data = logic_request.get("data", {})

        with open("logic_registry.json", "r") as f:
            routes = json.load(f)

        route = next((r for r in routes if r["logic_name"] == logic_name), None)
        if not route:
            return jsonify({"error": f"Logic '{logic_name}' not found."}), 404

        forwarded_response = requests.post(
            route["endpoint"],
            json=data,
            headers=get_headers()
        )

        return jsonify({
            "message": "Logic executed successfully.",
            "forwarded_response": forwarded_response.json()
        }), forwarded_response.status_code
    except Exception as e:
        logging.exception("Unexpected error in /run-logic")
        return jsonify({"error": "Internal server error"}), 500

@app.route("/log-idea", methods=["POST"])
def log_idea():
    try:
        data = request.get_json()
        idea = data.get("idea")
        category = data.get("category", "HydroCulture")
        type_ = data.get("type", "Wild Idea")

        if not idea:
            return jsonify({"error": "Missing idea"}), 400

        payload = {
            "parent": {"database_id": NOTION_DB_ID},
            "properties": {
                "Name": {
                    "title": [{"text": {"content": idea[:100]}}]
                },
                "Category": {"select": {"name": category}},
                "Type": {"select": {"name": type_}},
                "Created": {"date": {"start": datetime.now(timezone.utc).isoformat()}}
            }
        }

        response = requests.post(
            "https://api.notion.com/v1/pages",
            headers=get_headers(),
            json=payload
        )

        if not response.ok:
            logging.error(f"Notion API error: {response.text}")
            return jsonify({"error": "Notion API error", "details": response.text}), response.status_code

        return jsonify({"notion_response": response.json()}), 200
    except Exception as e:
        logging.exception("Unexpected error in /log-idea")
        return jsonify({"error": "Internal server error"}), 500

@app.route("/log-reflection", methods=["POST"])
def log_reflection():
    try:
        data = request.get_json()
        reflection = data.get("reflection")
        theme = data.get("theme", "Daily Insight")
        clarity = data.get("clarity_gained", "")
        next_action = data.get("next_action", "")

        payload = {
            "parent": {"database_id": REFLECTION_DB_ID},
            "properties": {
                "Reflection": {"rich_text": [{"text": {"content": reflection}}]},
                "Theme": {"select": {"name": theme}},
                "Clarity Gained": {"rich_text": [{"text": {"content": clarity}}]},
                "Next Action": {"rich_text": [{"text": {"content": next_action}}]},
                "Created": {"date": {"start": datetime.now(timezone.utc).isoformat()}}
            }
        }

        response = requests.post(
            "https://api.notion.com/v1/pages",
            headers=get_headers(),
            json=payload
        )

        if not response.ok:
            logging.error(f"Notion API error (reflection): {response.text}")
            return jsonify({"error": "Notion API error", "details": response.text}), response.status_code

        return jsonify({"notion_response": response.json()}), 200
    except Exception as e:
        logging.exception("Unexpected error in /log-reflection")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
