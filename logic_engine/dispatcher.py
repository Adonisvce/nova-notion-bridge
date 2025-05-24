# Dispatches logic commands to appropriate registered handlers
from logic_engine.registry import get_registered_logic
from logic_engine.utils import log_info

def dispatch_logic_command(command_name, payload):
    handler = get_registered_logic(command_name)
    if handler:
        log_info(f"Dispatching command: {command_name}")
        return handler(payload)
    else:
        raise ValueError(f"Unknown command: {command_name}")
