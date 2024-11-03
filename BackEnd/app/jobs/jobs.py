from app.jobs.worker import celery

@celery.task
def simpleTask():
    print("hello world!")
