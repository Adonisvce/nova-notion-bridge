# logic_engine/executor.py

from logic_engine.registry import plugin_registry

class LogicExecutor:
    def __init__(self):
        self.plugins = plugin_registry

    def execute(self, plugin_name, input_data):
        plugin_class = self.plugins.get(plugin_name)
        if not plugin_class:
            raise ValueError(f"Plugin '{plugin_name}' not found.")
        plugin_instance = plugin_class()
        return plugin_instance.run(input_data)
