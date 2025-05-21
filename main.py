
from flask import Flask, request, jsonify
import os
import requests
import logging
from datetime import datetime, timezone

# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# --- Environment Variables ---
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_DB_ID = os.getenv("NOTION_DB_ID")

app = Flask(__name__)

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
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

# --- Log Idea ---
@app.route("/log-idea", methods=["POST"])
def log_idea():
    try:
        data = request.get_json()
        idea = data.get("idea")
        category = data.get("category", "HydroCulture")
        type_ = data.get("type", "Wild Idea")

        logging.info(f"Received log-idea request: {data}")

        if not idea:
            logging.warning("Missing 'idea' in request")
            return jsonify({"error": "Missing idea"}), 400

        payload = {
            "parent": {"database_id": NOTION_DB_ID},
            "properties": {
                "Name": {
                    "title": [{
                        "type": "text",
                        "text": {"content": idea[:50]}
                    }]
                },
                "Category": {"select": {"name": category}},
                "Type": {"select": {"name": type_}},
                "Created": {
                    "date": {"start": datetime.now(timezone.utc).isoformat()}
                }
            }
        }

        response = requests.post("https://api.notion.com/v1/pages", headers=headers, json=payload)

        if not response.ok:
            logging.error(f"Notion API error: {response.text}")
            return jsonify({"error": "Notion API error", "details": response.text}), response.status_code

        logging.info("Idea successfully logged to Notion.")
        return jsonify({"notion_response": response.json()}), response.status_code

    except Exception as e:
        logging.exception("Unexpected error in /log-idea")
        return jsonify({"error": "Internal server error"}), 500

# --- Schedule Task ---
@app.route("/schedule", methods=["POST"])
def schedule_task():
    try:
        data = request.get_json()
        task = data.get("task")
        date = data.get("date")

        logging.info(f"Received schedule request: {data}")

        if not task or not date:
            logging.warning("Missing 'task' or 'date' in request")
            return jsonify({"error": "Missing task or date"}), 400

        return jsonify({
            "message": "Task scheduled",
            "task": task,
            "date": date
        }), 200

    except Exception as e:
        logging.exception("Unexpected error in /schedule")
        return jsonify({"error": "Internal server error"}), 500

# --- Get Ideas ---
@app.route("/get-ideas", methods=["GET"])
def get_ideas():
    # Placeholder response
    return jsonify({"ideas": ["Example idea 1", "Example idea 2"]}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
