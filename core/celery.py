from __future__ import absolute_import

import os

from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("core")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

app.conf.timezone = "Europe/Kiev"

# scheduled task execution
# app.conf.beat_schedule = {
# executes every odd hour
# "author-quote": {
#     "task": "quote.tasks.author_quote",
#     "schedule": crontab(minute=0, hour="1-23/2"),
# 'schedule': crontab(),
# }
# }


# Celery
# from datetime import timedelta
#
# from celery.schedules import crontab
#
# CELERY_TASK_RESULT_EXPIRES = 3600
#
# CELERY_BEAT_SCHEDULE = {
#     "celery.backend_cleanup": {
#         "task": "celery.backend_cleanup",
#         "schedule": timedelta(seconds=300),
#         "args": (),
#     },
#     "periodic": {
#         "task": "geo_data.tasks.add",
#         "schedule": timedelta(seconds=5),
#         "args": (4, 5),
#     },
# }
