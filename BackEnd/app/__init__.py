#app configureation and initialization

from flask import Flask
from .extensions import db, migrate, make_celery
from flask_cors import CORS
from config import Config
from .routes.api_routes import api_routes
from config import setup_logging
from flask_jwt_extended import JWTManager


def create_app():
    app = Flask(__name__)
    CORS(app)
    setup_logging(app)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(api_routes)
    celery = make_celery(app)

    app.extensions['celery'] = celery

    # Initialize JWT
    jwt = JWTManager(app)

    return app