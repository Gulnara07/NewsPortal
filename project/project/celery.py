import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

app = Celery('News')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.broker_connection_retry_on_startup = True

app.conf.beat_schedule = {
    'action_every_monday_8am': {
        'task': 'news.tasks.weekly_send_email_task',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
        'args': (),
    },
}