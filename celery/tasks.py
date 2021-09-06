from celery import Celery
from celery.result import AsyncResult

app = Celery('tasks', broker='redis://localhost:6379', backend='redis://localhost:6379')


@app.task()
def add(x, y):
    return x + y
