from app import create_app

app, celery = create_app()

celery.conf.update({ 'imports': ('app.jobs.jobs',), })


@celery.task
def test():
    return "test"