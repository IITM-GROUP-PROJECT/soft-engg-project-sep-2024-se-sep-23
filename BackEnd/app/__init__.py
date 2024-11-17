#app configureation and initialization

from flask import Flask
from .extensions import db, migrate
from config import Config
from .routes.api_routes import api_routes
from .routes.admin_routes import admin_routes
from .routes.professor_routes import professor_routes
from config import setup_logging
from flask_cors import CORS
from flask_jwt_extended import JWTManager

def create_app():
    app = Flask(__name__)

    setup_logging(app)
    app.config.from_object(Config)
    
    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(api_routes)
    app.register_blueprint(admin_routes, url_prefix='/api/admin')
    app.register_blueprint(professor_routes, url_prefix='/api')

    jwt = JWTManager(app)

    CORS(app)

    return app
