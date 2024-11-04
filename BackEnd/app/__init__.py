#app configureation and initialization

from flask import Flask
from .extensions import db, migrate, make_celery
from config import Config
from .routes.api_routes import api_routes
from config import setup_logging

from flask_jwt_extended import JWTManager

def create_app():
    app = Flask(__name__)

    setup_logging(app)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(api_routes)
    celery = make_celery(app)

    app.extensions['celery'] = celery

    # Initialize JWT
    app.config['JWT_SECRET_KEY'] = 'abcd_jwt_secret_key'
    jwt = JWTManager(app)

    return app