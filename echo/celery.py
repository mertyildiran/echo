from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings
import datetime

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'echo.settings')
app = Celery('echo')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

import django
django.setup()
from core.models import Echo

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(60.0, garbage_collector.s(), name='Garbage Collector')

@app.task
def garbage_collector():
    time_ago = datetime.datetime.now() - datetime.timedelta(minutes=5)

    echos = Echo.objects.filter(created_at__lte=time_ago, is_active=True).order_by('created_at')
    for echo in echos:
        if echo.audio and hasattr(echo.audio, 'path'):
            print(echo.audio.path)
            try:
                os.remove(echo.audio.path)
            except OSError:
                pass
        #echo.is_active = False
        #echo.save(update_fields=["is_active"])

    return True
