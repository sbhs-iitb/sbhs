from django.core.management.base import BaseCommand, CommandError
from sbhs_server import settings
from sbhs_server.tables.models import Board
from sbhs_server import helpers
import serial,time
from datetime import datetime

class Command(BaseCommand):
	args = ''
	help = 'Initializes the SBHS board data in the database'



	def handle(self, *args, **options):
		"""
		This function executes as a part of cron job . It monitors the condition of the SBHS devices. 
		To be specific it does the following checks : 
			1.It tries to connect to the devices whose path exists in map_machine_id.txt
			2.It checks the status of fan ,heater, sensor on SBHS by performing a series of variations on them and analysing 
				the result
		At the end it updates the Boards database with the device status.
		It mails the admin if any fault occurs.The mail comprises of machine Id of faulty board and probable cause.



		This function is invoked from command line as following
			python manage.py initialize_machines

		"""
		previous_onlines = Board.objects.only("mid").filter(online=True)
		previous_onlines = [p.mid for p in previous_onlines]
		current_onlines = settings.online_mids
		current_connections = settings.boards


		MINIMUM_DELTA = 1

		def write_to_sbhs(conn,command,value):
			conn.write(chr(command))
			conn.write(chr(value))

		def read_from_sbhs(conn,command):
			conn.write(chr(command))
			result=-1
			if command==255:
				result=ord(conn.read(1))+0.1*ord(conn.read(1))
			else:
				result=ord(conn.read(1))

			return result


		first_reading,second_reading,final_reading={},{},{}


		for key,value in current_connections.iteritems():
			first_reading[key]=read_from_sbhs(value['board'].boardcon,255)
			write_to_sbhs(value['board'].boardcon,253,0)
			write_to_sbhs(value['board'].boardcon,254,50)

		if len(current_connections.keys()) > 0:
			time.sleep(30)

		for key,value in current_connections.iteritems():
			second_reading[key] = read_from_sbhs(value['board'].boardcon,255)
			write_to_sbhs(value['board'].boardcon,253,100)

		if len(current_connections.keys()) > 0:
			time.sleep(50)

		for key,value in current_connections.iteritems():
			final_reading[key] = read_from_sbhs(value['board'].boardcon,255)


		for key,value in current_connections.iteritems():
			write_to_sbhs(value['board'].boardcon,253,100)
			write_to_sbhs(value['board'].boardcon,254,0)


		print first_reading
		print second_reading
		print final_reading



		delta1,delta2={},{}

		faulty_boards = {}

		for key in current_connections:
			delta1[key]=second_reading[key]-first_reading[key]
			delta2[key]=final_reading[key]-second_reading[key]

		for key in current_connections:
			if delta1[key] > MINIMUM_DELTA and delta2[key] < -MINIMUM_DELTA:
				pass
			elif delta1[key] > MINIMUM_DELTA and delta2[key] > MINIMUM_DELTA:
				#fans not working
				faulty_boards[key]="Probably Fan is not working"
			elif delta1[key] < MINIMUM_DELTA and delta2[key] < -MINIMUM_DELTA:
				#heaters not working
				faulty_boards[key]="Probably Heater is not working"
			else:
				#sensors not working
				faulty_boards[key]="Probably Sensor is not working"

		for o in current_onlines:
			try:
				Board.objects.get_or_create(mid=o)
			except:
				pass

		new_offlines = []
		for p in previous_onlines:
			if p not in current_onlines:
				new_offlines.append(p)


		message = "SBHS Administrator,\n\n"
		message += "Following issue requires immediate attention.\n\n"
		if len(new_offlines)>0:
			message += "SBHS could not be connected\n"
			for n in new_offlines:
				message += ("MID: %d\n" % n)
		if bool(faulty_boards):
			message += "Following devices are suspected to be faulty.\n\n"
			for key in faulty_boards:
					message += "MID : {}   Cause : {}\n" .format(key,faulty_boards[key])
		message += "\nYou can check the SBHS status on http://vlabs.iitb.ac.in/sbhs/admin/."
		message += " Possible correction actions are:\n"
		message += "1. Run this command without brackets -> ( cd $SBHS_SERVER_ROOT; ./new_cron_job.sh )\n"
		message += "2. If same machine comes offline multiple times, replacement of the machine is advised.\n\n\n"
		message += "Regards,\nSBHS Vlabs Server Code"

		print "New offline board mids", new_offlines
		subject = "SBHS Vlabs: Notice - SBHS not connected"

		try:
			if len(new_offlines) > 0 or len(faulty_boards)>0:
				for admin in settings.SBHS_ADMINS:
					helpers.mailer.email(admin[2], subject, message)
		except Exception as e:
			with open("mail_dump.txt", "a") as file:
				delimiter = " " + '#'*10 + " "
				file.write("\n" + delimiter + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + delimiter + "\n")
				file.write(message)
				print message


		Board.objects.filter(mid__in=current_onlines).update(online=True)
		Board.objects.exclude(mid__in=current_onlines).update(online=False)

		self.stdout.write('Boards loaded')
