from django.core.management.base import BaseCommand
from ...redis_client import reset_book_scores

class Command(BaseCommand):
    help = 'Reset book scores in Redis'

    def handle(self, *args, **kwargs):
        reset_book_scores()
        self.stdout.write(self.style.SUCCESS('Successfully reset book scores'))
