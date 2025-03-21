import json
from datetime import timedelta

from celery import shared_task
from django.utils import timezone
from django_celery_beat.models import IntervalSchedule, PeriodicTask

from .models import Kudos


@shared_task
def reset_kudos():
    """Deletes kudos older than 7 days to reset limits."""
    seven_days_ago = timezone.now() - timedelta(days=7)
    Kudos.objects.filter(timestamp__lte=seven_days_ago).delete()


schedule, created = IntervalSchedule.objects.get_or_create(
    every=7, period=IntervalSchedule.DAYS
)

PeriodicTask.objects.get_or_create(
    interval=schedule,
    name="Reset Kudos Count",
    task="kudosapp.tasks.reset_kudos",
    defaults={"args": json.dumps([])},
)