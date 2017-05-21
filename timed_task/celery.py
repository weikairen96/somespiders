from __future__ import absolute_import

from celery import Celery

app = Celery('timed_task', include=['timed_task.tasks'])

app.config_from_object('timed_task.celeryconfig')


if __name__ == '__main__':

    app.start()