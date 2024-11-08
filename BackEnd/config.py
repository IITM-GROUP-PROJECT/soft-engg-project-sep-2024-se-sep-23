import os
import logging
from dotenv import load_dotenv
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime
from celery.schedules import crontab


load_dotenv()

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
LOG_DIRECTORY = "logs"


if not os.path.exists(LOG_DIRECTORY):
    os.makedirs(LOG_DIRECTORY)

class CustomTimedRotatingFileHandler(TimedRotatingFileHandler):
    def doRollover(self):
        super().doRollover()
        new_file_name = "app_"+datetime.now().strftime("%Y-%m-%d") + ".log"
        old_file_path = self.baseFilename
        new_file_path = os.path.join(LOG_DIRECTORY, new_file_name)
        os.rename(old_file_path, new_file_path)


handler = CustomTimedRotatingFileHandler(
    filename=os.path.join(LOG_DIRECTORY, "app.log"),
    when="midnight",
    interval=1,
    backupCount=5,
)
handler.setLevel(LOG_LEVEL)
handler.setFormatter(logging.Formatter(
    "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"
))


def setup_logging(app):
    app.logger.setLevel(LOG_LEVEL)
    app.logger.addHandler(handler)


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL","sqlite:///app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY","SAF1AFDGGWE231A1AVPPROTJQMVRRW0PS76GH3PPTW1WAFN2GWQMVLTY041")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY","abcd_jwt_secret_key")

    CELERY = dict(
                    broker_url=os.getenv("REDIS_URL","redis://localhost:6379/0"),
                    result_backend=os.getenv("REDIS_URL","redis://localhost:6379/0"),
                    task_ignore_result=True,
                    # beat_schedule = {
                    #     'test-10-seconds-task':
                    #     {
                    #         'task': 'app.jobs.jobs.simpleTask',
                    #          'schedule': 10.0,  # every 10 seconds
                    #     },
                    #    'test-midnight-task':
                    #     {
                    #         'task': 'app.jobs.jobs.simpleTask',
                    #         'schedule': crontab(hour=0, minute=0),  # every midnight
                    #     },
                    # }
                )