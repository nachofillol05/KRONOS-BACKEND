from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()

class Command(BaseCommand):
    help = f'Creates a superuser automatically.'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING(f"Creating superuser..."))
        
        username = 'admin' #Modify these values as desired.
        email = 'admin@example.com'
        password = 'admin'

        if not User.objects.filter(document=username).exists():
            User.objects.create_superuser(document=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f"\nSuperuser '{username}' created successfully!\n"))
        else:
            self.stdout.write(self.style.ERROR(f"Superuser {username} already exists.\n"))
