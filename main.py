from flask import Flask, request, jsonify, redirect
from notion_client import Client
import os
import requests

app = Flask(__name__)

# Environment variables
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
REFLECTION_DB_ID = os.getenv("NOTION_REFLECTION_DB_ID")
LOGIC_CONFIG_DB_ID = os.getenv("NOTION_LOGIC_CONFIG_DB_ID")
COMMAND_CENTER_DB_ID = os.getenv("NOTION_COMMAND_CENTER_DB_ID")
OAUTH_CLIENT_ID = os.getenv("NOTION_CLIENT_ID")
OAUTH_CLIENT_SECRET = os.getenv("NOTION_CLIENT_SECRET")
OAUTH_REDIRECT_URI = os.getenv("OAUTH_REDIRECT_URI")

notion = Client(auth=NOTION_TOKEN)

@app.route("/")
def home():
    return "Nova OS is live", 200

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
    return jsonify(token_response.json())

@app.route("/sync-logic", methods=["POST"])
def sync_logic():
    try:
        logic_entries = notion.databases.query(database_id=LOGIC_CONFIG_DB_ID).get("results")
        endpoints = []

        for entry in logic_entries:
            props = entry["properties"]
            route = props.get("Route", {}).get("rich_text", [{}])[0].get("text", {}).get("content", "")
            method = props.get("Method", {}).get("select", {}).get("name", "POST").upper()
            logic = props.get("Logic", {}).get("rich_text", [{}])[0].get("text", {}).get("content", "")

            if not route or not logic:
                continue

            def dynamic_func(logic_block):
                def handler():
                    try:
                        local_vars = {}
                        exec(logic_block, {}, local_vars)
                        return jsonify(local_vars.get("response", {"message": "No response defined"}))
                    except Exception as e:
                        return jsonify({"error": str(e)}), 500
                return handler

            endpoint_func = dynamic_func(logic)
            endpoint_func.__name__ = f"{method}_{route.replace('/', '_')}"
            app.route(route, methods=[method])(endpoint_func)
            endpoints.append(route)

        return jsonify({"message": "Logic sync complete", "routes": endpoints}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/log-reflection", methods=["POST"])
def log_reflection():
    data = request.get_json()
    fields = {
        "Date": {"date": {"start": data.get("date")}},
        "Reflection": {"rich_text": [{"text": {"content": data.get("reflection")}}]},
        "Theme": {"select": {"name": data.get("theme")}},
        "Tags": {"multi_select": [{"name": tag} for tag in data.get("tags", [])]},
    }
    try:
        notion.pages.create(parent={"database_id": REFLECTION_DB_ID}, properties=fields)
        return jsonify({"message": "Reflection logged successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/update-command", methods=["POST", "PATCH", "DELETE"])
def update_command():
    data = request.get_json()
    command_id = data.get("id")
    try:
        if request.method == "POST":
            new_cmd = notion.pages.create(parent={"database_id": COMMAND_CENTER_DB_ID}, properties={
                "Command": {"title": [{"text": {"content": data.get("command")}}]},
                "Type": {"select": {"name": data.get("type")}},
                "Status": {"select": {"name": data.get("status", "Active")}},
            })
            return jsonify(new_cmd), 201
        elif request.method == "PATCH":
            notion.pages.update(page_id=command_id, properties={
                "Command": {"title": [{"text": {"content": data.get("command")}}]},
                "Type": {"select": {"name": data.get("type")}},
                "Status": {"select": {"name": data.get("status", "Active")}},
            })
            return jsonify({"message": "Command updated"}), 200
        elif request.method == "DELETE":
            notion.blocks.delete(block_id=command_id)
            return jsonify({"message": "Command deleted"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
