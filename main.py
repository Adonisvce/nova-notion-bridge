from flask import Flask, request, jsonify
from notion_client import Client
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
notion = Client(auth=os.getenv("NOTION_API_KEY"))

LOGIC_CONFIG_DB_ID = os.getenv("NOTION_LOGIC_CONFIG_DB_ID")

@app.route("/sync-logic", methods=["POST"])
def sync_logic():
    try:
        logic_config = notion.databases.query(database_id=LOGIC_CONFIG_DB_ID)

        for row in logic_config["results"]:
            properties = row["properties"]
            name = properties["Name"]["title"][0]["plain_text"] if properties["Name"]["title"] else ""
            path = properties["Path"]["rich_text"][0]["plain_text"] if properties["Path"]["rich_text"] else ""
            method = properties["Method"]["select"]["name"] if properties["Method"]["select"] else "POST"
            operation_id = properties["Operation ID"]["rich_text"][0]["plain_text"] if properties["Operation ID"]["rich_text"] else ""
            logic_code = properties["Logic"]["rich_text"][0]["plain_text"] if properties["Logic"]["rich_text"] else None
            enabled = properties["Enabled"]["checkbox"]
            endpoint = properties.get("Endpoint", {}).get("url", "")
            fields = properties.get("Fields", {}).get("rich_text", [])
            published = properties.get("Published", {}).get("checkbox", False)

            if not enabled or not published:
                continue

            field_schema = None
            if fields:
                try:
                    import json
                    field_schema = json.loads(fields[0]["plain_text"])
                except Exception as e:
                    print(f"Failed to parse fields for {name}: {e}")

            route_path = f"/{path.lstrip('/')}" if not endpoint else endpoint

            def make_handler(logic_code):
                def handler():
                    try:
                        local_vars = {}
                        exec(logic_code, globals(), local_vars)
                        return jsonify({"status": "success", "result": local_vars.get("result", "No result returned")})
                    except Exception as e:
                        return jsonify({"status": "error", "message": str(e)}), 500
                return handler

            app.route(route_path, methods=[method])(make_handler(logic_code))

        return jsonify({"status": "success", "message": "Logic synced successfully."})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
