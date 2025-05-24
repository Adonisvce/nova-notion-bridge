
class PluginRegistry:
    def __init__(self):
        self._registry = {}

    def register(self, name, plugin):
        self._registry[name] = plugin

    def get(self, name):
        return self._registry.get(name)

    def all(self):
        return self._registry

plugin_registry = PluginRegistry()
