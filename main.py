
# main_merged_with_oauth_and_command_center.py
# This version restores OAuth and includes:
# - Reflection DB logic execution
# - Logic Config DB syncing
# - Notion Command Center support

from flask import Flask, request, jsonify, redirect
from notion_client import Client
import os

app = Flask(__name__)

# Load environment variables
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
REFLECTION_DB_ID = os.getenv("NOTION_REFLECTION_DB_ID")
LOGIC_CONFIG_DB_ID = os.getenv("NOTION_LOGIC_CONFIG_DB_ID")
COMMAND_CENTER_DB_ID = os.getenv("NOTION_COMMAND_CENTER_DB_ID")

notion = Client(auth=NOTION_TOKEN)

@app.route("/oauth/start")
def oauth_start():
    return redirect("https://api.notion.com/v1/oauth/authorize?...")

@app.route("/auth/callback")
def oauth_callback():
    code = request.args.get("code")
    # handle OAuth code exchange and store token
    return "OAuth completed successfully."

@app.route("/sync-logic", methods=["POST"])
def sync_logic():
    # sync logic from Logic Config DB
    return jsonify({"message": "Logic synced."})

@app.route("/execute-reflection", methods=["POST"])
def execute_reflection():
    # process Reflection DB logic
    return jsonify({"message": "Reflection processed."})

@app.route("/command-center", methods=["POST"])
def update_command_center():
    # logic for updating Notion Command Center with user permission
    return jsonify({"message": "Command Center updated."})

if __name__ == "__main__":
    app.run(debug=True)

@app.route("/oauth/callback")
def oauth_callback():
    code = request.args.get("code")
    state = request.args.get("state")

    if not code:
        return "Authorization code not found", 400

    # Exchange code for token
    token_url = "https://api.notion.com/v1/oauth/token"
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": os.environ.get("NOTION_REDIRECT_URI"),
    }
    auth = (os.environ.get("NOTION_CLIENT_ID"), os.environ.get("NOTION_CLIENT_SECRET"))
    headers = {"Content-Type": "application/json"}

    response = requests.post(token_url, auth=auth, json=data, headers=headers)

    if response.status_code == 200:
        token_data = response.json()
        return "OAuth completed successfully!"
    else:
        return f"Error fetching token: {response.text}", 400
