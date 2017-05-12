from django.core.management.base import BaseCommand
from sbhs_server.tables.models import Experiment
import hashlib

class Command(BaseCommand):
    args = ''
    help = 'Calculates checksum for unchecked experiments'

    def handle(self, *args, **options):
        experiments = Experiment.objects.filter(checksum="NONE")

        for e in experiments:
            try:
                f = open(e.log, "r")
                # If log file doesn't exist, it means experiment is not done yet.
                # This takes care of that.
            except:
                return

            data = f.read()
            f.close()
            data = data.strip().split("\n")
            clean_data = ""
            for line in data:
                columns = line.split(" ")
                if len(columns) >= 6:
                    clean_data += (" ".join(columns[0:6]) + "\n")

            checksum = hashlib.sha1(clean_data).hexdigest()

            e.checksum = checksum
            e.save()
            print checksum
