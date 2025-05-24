from .command_center import register_command_center_routes
from .endpoint_router import register_endpoint_routes
# Uncomment below if plugin validation routes are defined
# from .plugin_validation import register_plugin_validation_routes

def register_all_routes(app):
    register_command_center_routes(app)
    register_endpoint_routes(app)
    # register_plugin_validation_routes(app)