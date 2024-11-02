#app configureation and initialization

from flask import Flask
from .extensions import db, migrate
from config import Config
from .routes.api_routes import api_routes
from config import setup_logging

def create_app():
    app = Flask(__name__)

    setup_logging(app)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(api_routes)

    return app
