
import importlib
import os
import pathlib

class LogicExecutor:
    def __init__(self, plugins_folder='logic_engine/plugins'):
        self.plugins_folder = plugins_folder
        self.plugins = self.load_plugins()

    def load_plugins(self):
        plugins = {}
        plugin_path = pathlib.Path(self.plugins_folder)
        for file in plugin_path.glob("*.py"):
            if file.name == "__init__.py":
                continue
            module_name = f"logic_engine.plugins.{file.stem}"
            module = importlib.import_module(module_name)
            if hasattr(module, "execute"):
                plugins[file.stem] = module
        return plugins

    def execute(self, plugin_name, **kwargs):
        plugin = self.plugins.get(plugin_name)
        if not plugin:
            raise ValueError(f"Plugin '{plugin_name}' not found.")
        return plugin.execute(**kwargs)

executor = LogicExecutor()
