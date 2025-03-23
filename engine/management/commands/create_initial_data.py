from django.core.management.base import BaseCommand
from engine.utils import create_initial_data  # Replace 'engine' with your app name

class Command(BaseCommand):
    help = 'Creates initial roles and users.'

    def handle(self, *args, **options):
        create_initial_data()
        self.stdout.write(self.style.SUCCESS('Successfully created initial data.'))