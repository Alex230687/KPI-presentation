import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'KPI.settings')

app = Celery('KPI')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


# $ celery -A KPI beat -l info
app.conf.beat_schedule = {
    'update-database-every-week': {
        'task': 'main.tasks.beat_update_database_data',
        'schedule': crontab(
            minute=0,
            hour='9,18',
            day_of_week='saturday'
        ),
    }
}