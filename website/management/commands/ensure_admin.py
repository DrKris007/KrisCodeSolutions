import os
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Create or reset the admin user from environment variables"

    def handle(self, *args, **options):
        username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "")
        if not username or not password:
            raise CommandError("Set DJANGO_SUPERUSER_USERNAME and DJANGO_SUPERUSER_PASSWORD")

        User = get_user_model()
        user, _ = User.objects.get_or_create(**{User.USERNAME_FIELD: username})
        if email and hasattr(user, "email"):
            user.email = email
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save()
        self.stdout.write(self.style.SUCCESS("Admin user ready"))
