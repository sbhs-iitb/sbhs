from django.core.management.base import BaseCommand, CommandError
from sbhs_server import settings, helpers
import os, json

class Command(BaseCommand):
	args = ''
	help = 'Sends email to admin'



	def handle(self, *args, **options):
		
		# Store all Raspberry Pi IP's in a list
		with open(os.path.join(settings.BASE_DIR, "sbhs_server/RPi_data/ipaddrs.txt"), "r") as filehandler:
			ipaddrs = filehandler.readlines()

		# Strip whitespaces (in case)
		ipaddrs = [ip.strip() for ip in ipaddrs]

		new_offlines = []
		faulty_boards = {}

		# Create data for offline and faulty boards
		for ip in ipaddrs:
			filename = "sbhs_server/RPi_data/report/" + ip + ".txt"
			with open(os.path.join(settings.BASE_DIR, filename), "r") as filehandler:
				data = filehandler.read()
			data = json.loads(data)
			new_offlines += data["new_offlines"]
			faulty_boards.update(data["faulty_boards"])

		# Compose body for the email
		message = "SBHS Administrator,\n\n"
		message += "Following issue requires immidiate attention.\n\n"
		if len(new_offlines) > 0:
			message += "SBHS could not be connected\n"
			for n in new_offlines:
				message += ("MID: %d\n" % n)
		if bool(faulty_boards):
			message += "Following devices are suspected to be faulty.\n\n"
			for key in faulty_boards:
					message += "MID : {}   Cause : {}\n" .format(key,faulty_boards[key])
		message += "\nYou can check the SBHS status on http://vlabs.iitb.ac.in/sbhs/admin/."
		message += " Possible correction actions are:\n"
		message += "1. Run this command without brackets -> ( cd $SBHS_SERVER_ROOT; ./cron_job.sh )\n"
		message += "2. If same machine comes offline multiple times, replacement of the machine is advised.\n\n\n"
		message += "Regards,\nSBHS Vlabs Server Code"

		print "New offline board mids", new_offlines
		subject = "SBHS Vlabs: Notice - SBHS not connected"

		# Send email
		if len(new_offlines) > 0 or len(faulty_boards)>0:
			for admin in settings.SBHS_ADMINS:
				helpers.mailer.email(admin[2], subject, message)