import subprocess
import sys
import time


def start_flask():
    subprocess.run([sys.executable, "run.py"])


def start_celery_worker():
    subprocess.Popen([sys.executable, "-m", "celery", "-A", "app.jobs.worker.celery", "worker", "--loglevel=info"])


def start_celery_beat():
    subprocess.Popen([sys.executable, "-m", "celery", "-A", "app.jobs.worker.celery", "beat", "--loglevel=info"])


if __name__ == "__main__":
    start_celery_worker()
    start_celery_beat()

    time.sleep(2)

    start_flask()
