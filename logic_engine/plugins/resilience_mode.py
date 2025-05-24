from logic_engine.plugin_base import LogicPlugin

class ResilienceModePlugin(LogicPlugin):
    def run(self, data=None):
        mood = data.get("mood", "unknown")
        if mood in ["low", "anxious", "overwhelmed"]:
            return {
                "mode": "resilience",
                "message": "Nova’s here. Take a breath. Let's tackle one thing at a time.",
                "tips": [
                    "Minimize distractions for 15 mins",
                    "Do a brain dump in Notion",
                    "Let’s review your M.E.L. goals"
                ]
            }
        return {"mode": "normal", "message": "Resilience Mode not needed."}