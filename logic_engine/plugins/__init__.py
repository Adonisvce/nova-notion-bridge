
from logic_engine.plugin_base import LogicPlugin
import importlib
import pkgutil

# Automatically discover and register plugins
plugin_registry = {}

def load_plugins():
    package = __name__
    for loader, name, is_pkg in pkgutil.iter_modules(__path__, package + "."):
        module = importlib.import_module(name)
        for attr in dir(module):
            obj = getattr(module, attr)
            if isinstance(obj, type) and issubclass(obj, LogicPlugin) and obj is not LogicPlugin:
                plugin_registry[obj.__name__] = obj

load_plugins()
