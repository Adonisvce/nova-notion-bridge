from logic_engine.plugin_base import LogicPlugin

class NotionSyncCheckPlugin(LogicPlugin):
    def run(self, data=None):
        notion_state = data.get("notion_state", {})
        if not notion_state.get("last_synced") or notion_state.get("has_changes", False):
            return {"action": "sync", "reason": "Detected changes in Notion"}
        return {"action": "skip", "reason": "No changes detected"}