import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE','pureearth.settings')

app=Celery('pureearth')
app.config_from_object('django.conf:settings',namespace='CELERY')
app.autodiscover_tasks()
