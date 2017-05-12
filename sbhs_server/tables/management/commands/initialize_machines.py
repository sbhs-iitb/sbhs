from django.core.management.base import BaseCommand, CommandError
from sbhs_server import settings
from sbhs_server.tables.models import Board
from sbhs_server import helpers

class Command(BaseCommand):
    args = ''
    help = 'Initializes the SBHS board data in the database'

    def handle(self, *args, **options):
        previous_onlines = Board.objects.only("mid").filter(online=True)
        previous_onlines = [p.mid for p in previous_onlines]
        for o in settings.online_mids:
            try:
                Board.objects.get_or_create(mid=o)
            except:
                pass

        new_offlines = []
        for p in previous_onlines:
            if p not in settings.online_mids:
                new_offlines.append(p)

        message = "SBHS Administrator,\n\n"
        message += "Following issue requires immidiate attention.\n\n"
        message += "SBHS could not be connected\n"
        for n in new_offlines:
            message += ("MID: %d\n" % n)
        message += "\nYou can check the SBHS status on http://vlabs.iitb.ac.in/sbhs/admin/."
        message += " Possible correction actions are:\n"
        message += "1. Run this command without brackets -> ( cd $SBHS_SERVER_ROOT; ./cron_job.sh )\n"
        message += "2. If same machine comes offline multiple times, replacement of the machine is advised.\n\n\n"
        message += "Regards,\nSBHS Vlabs Server Code"

        print "New offline board mids", new_offlines
        subject = "SBHS Vlabs: Notice - SBHS not connected"

        if len(new_offlines) > 0:
            for admin in settings.SBHS_ADMINS:
                helpers.mailer.email(admin[2], subject, message)

        Board.objects.filter(mid__in=settings.online_mids).update(online=True)
        Board.objects.exclude(mid__in=settings.online_mids).update(online=False)

        self.stdout.write('Boards loaded')
