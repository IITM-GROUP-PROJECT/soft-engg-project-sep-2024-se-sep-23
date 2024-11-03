from app.jobs.worker import celery

@celery.task
def simpleTask():
    return "hello world!"
