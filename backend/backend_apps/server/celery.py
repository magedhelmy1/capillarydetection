import os

from celery import Celery
from kombu import Exchange, Queue

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')

app = Celery('server')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
worker_send_task_event = False
task_ignore_result = True

# # task will be killed after 60 seconds
# task_time_limit = 60
# # task will raise exception SoftTimeLimitExceeded after 50 seconds
# task_soft_time_limit = 50
# # task messages will be acknowledged after the task has been executed, not just before (the default behavior).
# task_acks_late = True
# # One worker taks 10 tasks from queue at a time and will increase the performance
worker_prefetch_multiplier = 10

# task_queues = (
#     Queue('celery', routing_key='celery'),
#     Queue('transient', Exchange('transient', delivery_mode=1),
#           routing_key='transient', durable=False),
# )

# app.conf.task_default_queue = 'default'
# app.conf.task_queues = (
#     Queue('celery', routing_key='celery'),
#     Queue('transient', Exchange('transient', delivery_mode=1),
#           routing_key='transient', durable=False),
# )
# app.conf.task_default_exchange = 'tasks'
# app.conf.task_default_exchange_type = 'topic'
# app.conf.task_default_routing_key = 'task.default'
# app.conf.BROKER_TRANSPORT_OPTIONS = {"max_retries": 10, "interval_start": 1, "interval_step": 3, "interval_max": 60}
# task_acks_late = True
# worker_prefetch_multiplier = 0


# @app.task(bind=True)
# def debug_task(self):
#     print(f'Request: {self.request!r}')
