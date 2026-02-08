from flask import Flask


def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.json.sort_keys = False

    from app.routes.auth import auth_bp
    from app.routes.user import user_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)

    return app