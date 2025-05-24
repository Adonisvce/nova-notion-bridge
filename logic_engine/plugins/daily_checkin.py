from logic_engine.plugin_base import LogicPlugin

class DailyCheckinPlugin(LogicPlugin):
    def run(self, data=None):
        return {
            "status": "ok",
            "message": "Good morning! Nova is online and ready.",
            "next_steps": ["Check Notion for updates", "Run sync if changes exist"]
        }