#Dev/KoDe :)

import csv
import datetime
import os
import sys
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    args = ''
    help = 'Creates Log'

    def handle(self, *args, **options):
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sbhs_server.settings") # To make a Django Environment.

        from sbhs_server.tables.models import Board
        board_details = Board.objects.values_list("online", flat=True)
        board = str([x for x in board_details])
        with open('new.csv', "a") as newcsv:
            newcsv.write("{0} {1} \n".format(datetime.datetime.now(), board.replace(",", "").replace("[", "").replace("]","")))
