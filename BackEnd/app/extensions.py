#all import extension should be created here and imported to other modules
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from celery import Celery

db = SQLAlchemy()
migrate = Migrate()

def make_celery(app):
    celery = Celery(app.import_name)
    celery.config_from_object(app.config["CELERY"])
    return celery

