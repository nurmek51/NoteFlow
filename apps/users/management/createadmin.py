from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

class Command(BaseCommand):
    help = "Создает суперпользователя, если он не существует"

    def handle(self, *args, **options):
        User = get_user_model()
        username = os.environ.get('ADMIN_USERNAME')
        email = os.environ.get('ADMIN_EMAIL')
        password = os.environ.get('ADMIN_PASSWORD')

        if not username or not email or not password:
            self.stdout.write("Пожалуйста, установите переменные окружения ADMIN_USERNAME, ADMIN_EMAIL и ADMIN_PASSWORD.")
            return

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS("Суперпользователь создан."))
        else:
            self.stdout.write("Суперпользователь уже существует.")
