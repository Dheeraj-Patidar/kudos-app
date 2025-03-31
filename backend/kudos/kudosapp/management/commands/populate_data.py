import random

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from kudosapp.models import Kudos, Organization


class Command(BaseCommand):
    help = "Creates an admin user, 5 regular users, and some kudos"

    def handle(self, *args, **kwargs):
        User = get_user_model()

        # Create Organization
        org, _ = Organization.objects.get_or_create(name="Tech Corp")

        # Create Admin User
        admin_email = "admin@gmail.com"
        if not User.objects.filter(email=admin_email).exists():
            User.objects.create_superuser(
                email=admin_email, password="admin@123"
            )
            self.stdout.write(
                self.style.SUCCESS(f"Admin user created: {admin_email}")
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f"Admin user already exists: {admin_email}")
            )

        users = []
        for i in range(1, 6):
            email = f"user{i}@gmail.com"
            if not User.objects.filter(email=email).exists():
                user = User.objects.create_user(
                    email=email, first_name="user", last_name=f"{i}", password=f"user{i}@123", organization=org
                )
                users.append(user)
                self.stdout.write(self.style.SUCCESS(f"User created: {email}"))
            else:
                self.stdout.write(
                    self.style.SUCCESS(f"User already exists: {email}")
                )

        # Create Kudos
        for _ in range(10):
            sender = random.choice(users)
            receiver = random.choice(
                [user for user in users if user != sender]
            )
            Kudos.objects.create(
                sender=sender, sender_first_name=sender.first_name,
                sender_last_name=sender.last_name,
                receiver=receiver, message="Great job!"
            )
        self.stdout.write(self.style.SUCCESS("Kudos created!"))
