from flask import Flask
from celery import Celery
from src.config import Config


celery_app = Celery("celery", broker=Config.CELERY_BROKER_URL, backend=Config.CELERY_BACKEND_URL)


def init_celery(app: Flask):
    """Create Celery app"""

    task_base = celery_app.Task

    class ContextTask(task_base):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return task_base.__call__(self, *args, **kwargs)

    celery_app.Task = ContextTask

    app.extensions["celery"] = celery_app
