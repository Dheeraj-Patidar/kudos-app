import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kudos.settings")

app = Celery("kudos")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.enable_utc = False  # Disable UTC
app.conf.timezone = "Asia/Kolkata"  # Change to your local timezone

app.autodiscover_tasks()
