from .endpoint_router import register_endpoint_routes
from .command_center import register_command_center_routes

def register_all_routes(app):
    register_endpoint_routes(app)
    register_command_center_routes(app)
