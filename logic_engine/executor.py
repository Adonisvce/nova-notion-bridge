
import importlib
import os
import pkgutil
from logic_engine.plugin_base import LogicPlugin

class LogicExecutor:
    def __init__(self):
        self.plugins = self.load_plugins()

    def load_plugins(self):
        plugins = {}
        package_dir = os.path.dirname(__file__)
        for _, name, _ in pkgutil.iter_modules([os.path.join(package_dir, 'plugins')]):
            module_name = f"logic_engine.plugins.{name}"
            module = importlib.import_module(module_name)
            plugin_class = getattr(module, "Plugin", None)
            if plugin_class and issubclass(plugin_class, LogicPlugin):
                plugins[name] = plugin_class()
        return plugins

    def execute(self, plugin_name, data):
        if plugin_name in self.plugins:
            return self.plugins[plugin_name].run(data)
        else:
            raise ValueError(f"Plugin '{plugin_name}' not found.")

# Instantiate executor and expose the execute_logic function
executor = LogicExecutor()

def execute_logic(plugin_name, data):
    return executor.execute(plugin_name, data)
