from routes.command_center import command_center_bp
from routes.endpoint_router import endpoint_router_bp
from routes.dynamic import dynamic_bp
from routes.validate_plugins import validate_bp
from routes.oauth import oauth_bp

def register_all_routes(app):
    app.register_blueprint(command_center_bp)
    app.register_blueprint(endpoint_router_bp)
    app.register_blueprint(dynamic_bp)
    app.register_blueprint(validate_bp)
    app.register_blueprint(oauth_bp)
