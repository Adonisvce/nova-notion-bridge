# logic_engine/plugin_registry.py

hook_registry = {
    "before_logic": [],
    "after_logic": [],
    "startup": [],
    "shutdown": [],
}

def run_hooks(hook_name, *args, **kwargs):
    for hook in hook_registry.get(hook_name, []):
        hook(*args, **kwargs)
