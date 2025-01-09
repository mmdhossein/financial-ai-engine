from flask import Flask
from app.routes import router

def create_app():
    app = Flask(__name__)

    # Configuration
    app.config.from_object("app.config.Config")

    # env = os.environ.get("FLASK_ENV", "development")
    # if env == "production":
    #     app.config.from_object("app.config.ProductionConfig")
    # elif env == "testing":
    #     app.config.from_object("app.config.TestingConfig")
    # else:
    #     app.config.from_object("app.config.DevelopmentConfig")

    # Register the router
    app.register_blueprint(router, url_prefix="/api/ai/engine")

    return app
