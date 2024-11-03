from app import create_app

app = create_app()

celery = app.extensions['celery']
celery.conf.update({ 'imports': ('app.jobs.jobs',), })


@celery.task
def test():
    return "test"