import os

from celery import Celery

worker_send_task_event = False
task_ignore_result = True
task_time_limit = 60
task_soft_time_limit = 50
task_acks_late = True
worker_prefetch_multiplier = 2

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')

app = Celery('server')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# @app.task(bind=True)
# def debug_task(self):
#     print(f'Request: {self.request!r}')
