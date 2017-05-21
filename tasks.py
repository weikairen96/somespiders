import time
from celery import Celery

app = Celery('tasks', broker='redis://localhost:6379/0')

from datetime import timedelta



app.conf.update(
CELERYBEAT_SCHEDULE = {
    'add-every-30-seconds': {
        'task': 'tasks.add',
        'schedule': timedelta(seconds=30),
        'args': (16, 16)
    },
},

CELERY_TIMEZONE = 'UTC'
)
@app.task
def add(x, y):
    return x + y