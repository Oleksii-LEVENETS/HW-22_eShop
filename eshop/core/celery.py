from __future__ import absolute_import, unicode_literals

import os
from datetime import timedelta

from celery import Celery
from celery.schedules import crontab  # noqa: F401

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("core")

app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

app.conf.timezone = "Europe/Kiev"

# scheduled task execution
app.conf.beat_schedule = {
    # executes every 5 minutes
    "synchro_db": {
        "task": "orders.tasks.synchro_db",
        # "schedule": crontab(minute="*/5"),
        "schedule": timedelta(seconds=10),
    }
}
