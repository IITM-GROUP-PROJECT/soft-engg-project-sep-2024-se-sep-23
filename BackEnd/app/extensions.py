#all import extension should be created here and imported to other modules

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail

db = SQLAlchemy()
migrate = Migrate()
mail = Mail()