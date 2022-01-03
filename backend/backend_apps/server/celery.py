import os

from celery import Celery
from kombu import Exchange, Queue

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')

app = Celery('server')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

task_routes = {
    'proj.tasks.add': {'queue': 'celery', 'delivery_mode': 'transient'}
}

# worker_prefetch_multiplier = 0


# @app.task(bind=True)
# def debug_task(self):
#     print(f'Request: {self.request!r}')
