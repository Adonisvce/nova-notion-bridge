# Registry of available logic actions and handlers
from logic_engine.utils import log_info

LOGIC_REGISTRY = {}

def register_logic(name, handler):
    LOGIC_REGISTRY[name] = handler
    log_info(f"Registered logic: {name}")

def get_registered_logic(name):
    return LOGIC_REGISTRY.get(name)
