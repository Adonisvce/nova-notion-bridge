
# logic_engine/registry.py

plugin_registry = {}

def register_plugin(name, func):
    plugin_registry[name] = func

def get_plugin(name):
    return plugin_registry.get(name)

def list_plugins():
    return list(plugin_registry.keys())
