from routes.command_center import register_command_center_routes
from routes.endpoint_router import register_endpoint_routes

def register_all_routes(app, notion):
    register_command_center_routes(app, notion)
    register_endpoint_routes(app, notion)