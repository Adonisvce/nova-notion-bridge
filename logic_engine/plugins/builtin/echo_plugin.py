from logic_engine.plugin_base import LogicPlugin

class EchoPlugin(LogicPlugin):
    def run(self, data: dict) -> dict:
        return {"response": data.get("message", "No message received.")}