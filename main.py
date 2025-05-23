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

# --- Headers using saved token ---
def get_headers():
    token_data = load_token()
    access_token = token_data.get("access_token")
    return {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }

# --- Health Check ---
@app.route("/status", methods=["GET"])
def status():
    return jsonify({"status": "ok"}), 200

# --- Home ---
@app.route("/")
def home():
    return "✅ Nova Notion Bridge is live."

# --- OAuth Start ---
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

# --- OAuth Callback ---
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

# --- Get Token (for debug) ---
@app.route("/auth/token", methods=["GET"])
def get_token():
    return jsonify(load_token())

# --- Log Idea ---
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
                "Name": {"title": [{"text": {"content": idea[:50]}}]},
                "Category": {"select": {"name": category}},
                "Type": {"select": {"name": type_}},
                "Created": {"date": {"start": datetime.now(timezone.utc).isoformat()}}
            }
        }

        response = requests.post("https://api.notion.com/v1/pages", headers=get_headers(), json=payload)

        if not response.ok:
            logging.error(f"Notion API error: {response.text}")
            return jsonify({"error": "Notion API error", "details": response.text}), response.status_code

        return jsonify({"notion_response": response.json()}), 200

    except Exception as e:
        logging.exception("Unexpected error in /log-idea")
        return jsonify({"error": "Internal server error"}), 500

# --- Log Milestone ---
@app.route("/log-milestone", methods=["POST"])
def log_milestone():
    try:
        logging.info(f"DEBUG - Using NOTION_DB_ID: {NOTION_DB_ID}")  # Debug log to confirm DB ID
        
        data = request.get_json()
        task = data.get("task")
        category = data.get("category", "General")
        timeframe = data.get("timeframe", "Short-Term")

        if not task:
            return jsonify({"error": "Missing task"}), 400

        payload = {
            "parent": {"database_id": NOTION_DB_ID},
            "properties": {
                "Task": {"title": [{"text": {"content": task[:100]}}]},
                "Category": {"select": {"name": category}},
                "Timeframe": {"select": {"name": timeframe}},
                "Created": {"date": {"start": datetime.now(timezone.utc).isoformat()}}
            }
        }

        response = requests.post("https://api.notion.com/v1/pages", headers=get_headers(), json=payload)

        if not response.ok:
            logging.error(f"Notion API error (milestone): {response.text}")
            return jsonify({"error": "Notion API error", "details": response.text}), response.status_code

        return jsonify({"notion_response": response.json()}), 200

    except Exception as e:
        logging.exception("Unexpected error in /log-milestone")
        return jsonify({"error": "Internal server error"}), 500

# --- Schedule Task (Placeholder) ---
@app.route("/schedule", methods=["POST"])
def schedule_task():
    try:
        data = request.get_json()
        task = data.get("task")
        date = data.get("date")

        if not task or not date:
            return jsonify({"error": "Missing task or date"}), 400

        return jsonify({"message": "Task scheduled", "task": task, "date": date}), 200

    except Exception as e:
        logging.exception("Unexpected error in /schedule")
        return jsonify({"error": "Internal server error"}), 500

# --- Get Ideas (Placeholder) ---
@app.route("/get-ideas", methods=["GET"])
def get_ideas():
    return jsonify({"ideas": ["Example idea 1", "Example idea 2"]}), 200

# --- Run App ---
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
