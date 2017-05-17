from django.core.management.base import BaseCommand
from sbhs_server.tables.models import Board
from sbhs_server.webcam.views import load_image

class Command(BaseCommand):
    args = ''
    help = 'Reloads images for all SBHS machines'

    def handle(self, *args, **options):
        boards = Board.objects.all()
        for b in boards:
            load_image(b.mid)
