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
    logging.info(

