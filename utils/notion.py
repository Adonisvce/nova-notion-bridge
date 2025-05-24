import os
from notion_client import Client
from dotenv import load_dotenv

load_dotenv()

notion = Client(auth=os.getenv("NOTION_API_KEY"))

def get_database_items(database_id: str):
    try:
        response = notion.databases.query(database_id=database_id)
        return response["results"]
    except Exception as e:
        print(f"Error querying Notion database: {e}")
        return []
