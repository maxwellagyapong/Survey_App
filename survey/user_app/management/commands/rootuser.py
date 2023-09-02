from django.core.management import BaseCommand
from user_app.models import User

"""Script responsible for creating root user"""

class Command(BaseCommand):
    help = "Runs all query commands"

    def handle(self, *args, **options):
        User.objects.create(username='master', password='keypass')