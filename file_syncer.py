
import os
import hashlib
import requests
import json
from datetime import datetime

# === CONFIG ===
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_DATABASE_ID = os.getenv("NOTION_FILE_TRACKER_DB")
NOTION_VERSION = "2022-06-28"
SYNCED_FILES = [
    "main.py",
    "logic_syncer.py",
    "requirements.txt",
    ".env",
    "pyproject.toml",
    "notion_config.json"
]

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": NOTION_VERSION,
    "Content-Type": "application/json"
}

def hash_file(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def get_last_hash_from_notion(file_name):
    query_url = f"https://api.notion.com/v1/databases/{NOTION_DATABASE_ID}/query"
    response = requests.post(query_url, headers=headers)
    response.raise_for_status()
    data = response.json()

    for result in data.get("results", []):
        props = result["properties"]
        if props["File Name"]["title"][0]["text"]["content"] == file_name:
            return props["SHA256"]["rich_text"][0]["text"]["content"]
    return None

def update_notion_record(file_name, sha, modified_time):
    query_url = f"https://api.notion.com/v1/databases/{NOTION_DATABASE_ID}/query"
    response = requests.post(query_url, headers=headers)
    response.raise_for_status()
    data = response.json()

    page_id = None
    for result in data.get("results", []):
        props = result["properties"]
        if props["File Name"]["title"][0]["text"]["content"] == file_name:
            page_id = result["id"]
            break

    body = {
        "properties": {
            "File Name": {"title": [{"text": {"content": file_name}}]},
            "SHA256": {"rich_text": [{"text": {"content": sha}}]},
            "Last Modified": {"date": {"start": modified_time}}
        }
    }

    if page_id:
        requests.patch(f"https://api.notion.com/v1/pages/{page_id}", headers=headers, json=body)
    else:
        body["parent"] = {"database_id": NOTION_DATABASE_ID}
        requests.post("https://api.notion.com/v1/pages", headers=headers, json=body)

def sync_files():
    for file in SYNCED_FILES:
        if not os.path.isfile(file):
            print(f"⚠️ Missing file: {file}")
            continue

        sha = hash_file(file)
        modified_time = datetime.fromtimestamp(os.path.getmtime(file)).isoformat()
        last_sha = get_last_hash_from_notion(file)

        if sha != last_sha:
            print(f"🔄 Updating {file} in Notion...")
            update_notion_record(file, sha, modified_time)
        else:
            print(f"✅ {file} is already up to date.")

if __name__ == "__main__":
    sync_files()
