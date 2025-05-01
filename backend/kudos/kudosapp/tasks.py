from datetime import timedelta

from celery import shared_task
from django.contrib.auth import get_user_model
from django.utils.timezone import now

User = get_user_model()


@shared_task
def reset_kudos_count():
    """Reset the kudos count for all users without deleting old kudos."""
    seven_days_ago = now() - timedelta(days=7)
    User.objects.filter(kudos_last_reset__lt=seven_days_ago).update(
        kudos_count=3, kudos_last_reset=now()
    )


# from celery import shared_task
# from django.utils.timezone import now
# from datetime import timedelta
# from kudosapp.models import User
# import pytz  # Add timezone support

# @shared_task
# def reset_kudos_count():
#     """Reset kudos count every 2 minutes."""
#     ist = pytz.timezone("Asia/Kolkata")  # Ensure IST timezone

#     current_time = now().astimezone(ist)
#     two_minutes_ago = current_time - timedelta(minutes=2)

#     users_updated = User.objects.filter(
#         kudos_last_reset__lt=two_minutes_ago
#     ).update(kudos_count=3, kudos_last_reset=current_time)  # Update reset time

#     print(f"Kudos reset for {users_updated} users at {current_time}")  # Debugging log
