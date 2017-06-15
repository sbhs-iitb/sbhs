import htmlPy
from htmlPy import Bridge, attach
import urllib2, cookielib, urllib
import time
import os, json, sys, logging
from threading import Thread
logging.basicConfig(level=logging.DEBUG)

global_cur_heat = 0
global_cur_fan = 0
global_cur_temp = 0
global_iter = 0
global_remaining_time = 0
global_error = ""

class SBHSClient(Bridge):
	def __init__(self):

		self.path = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.realpath(__file__))
		super(SBHSClient, self).__init__()
		self.app = htmlPy.AppWindow(title="SBHS Vlabs Client", width=360, height=600, x_pos=32, y_pos=32)
		self.app.window.setFixedSize(360, 600)
		try:
			config_options = {}
			with open(os.path.join(self.path, "config.txt")) as f:
				logging.debug("config.txt present. Loading configuration.")
				for line in f:
					if len(line.strip()) > 2:
						opt = line.split(":")
						config_options[opt[0].strip()] = opt[1].strip()

			if config_options["base_link"] != "None" and len(config_options["base_link"]) > 2:
				link = config_options["base_link"]
			else:
				link = "http://vlabs.iitb.ac.in/"
		#############################################
			link = "http://192.168.43.144/sbhs/"
			if config_options["use_proxy"] != "Yes":
				proxy_handler = urllib2.ProxyHandler({})
				logging.debug("Proxy: None")
			else:
				logging.debug("Loading proxy.")
				proxy_url = config_options["proxy_type"] + "://"
				proxy_url += (urllib.quote(config_options["proxy_username"]) + ":" if config_options["proxy_username"] != "" else "")
				proxy_url += (urllib.quote(config_options["proxy_password"]) + "@" if config_options["proxy_username"] != "" else "")
				proxy_url += config_options["proxy_host"] + ":"
				proxy_url += config_options["proxy_port"] + "/"
				proxy_handler = urllib2.ProxyHandler({config_options["proxy_type"]: proxy_url})
				logging.debug("Proxy: " + config_options["proxy_type"] + ": " + proxy_url)
			logging.debug("BASE_LINK: " + link)
		except Exception:
			logging.exception("Error while loading config. Switching to default configuration.")
			link = "http://vlabs.iitb.ac.in/"
		#############################################
			link = "http://192.168.43.144/sbhs/"
			proxy_handler = urllib2.ProxyHandler({})
			logging.debug("Proxy: None")
			logging.debug("BASE_LINK: " + link)

		self.base_url = link + "experiment/"
		self.version = "3"
		self.urllib2 = urllib2
		self.logdir = "logs"
		self.scilabreadfname = "scilabread.sce"
		self.scilabwritefname = "scilabwrite.sce"
		self.cur_heat = 0
		self.cur_fan = 0
		self.cur_temp = 0
		self.iter = 0
		self.remaining_time = 0
		self.error = ""
		self.status = False
		self.machine_ip=""#ADDED
		self.machine_url=""#ADDED
		self.link = link

		cookie_support = cookielib.CookieJar()
		opener = urllib2.build_opener(proxy_handler, urllib2.HTTPCookieProcessor(cookie_support))
		self.urllib2.install_opener(opener)

		self.app.setTemplatePath(self.path)

	@attach(result=str)
	def check_connection(self):
		try:
			print self.base_url+"check_connection"
			br = urllib2.urlopen(self.base_url + "check_connection")
			return br.read()
		except Exception:
			logging.exception("Failed in checking server connection")
			return "NO"

	@attach(result=bool)
	def client_version(self):
		try:
			br = urllib2.urlopen(self.base_url + "client_version")
			return br.read() == self.version
		except Exception:
			logging.exception("Failed in checking client version")
			return False

	@attach(str, str, result=str)
	def authenticate(self, username, password):
		try:
			username = str(username)
			password = str(password)

			input_data = urllib.urlencode({"username": username, "password": password})
			
			ip_req = self.urllib2.Request(self.base_url + "initiate", input_data) 
			json_response = urllib2.urlopen(ip_req)

			data = json.loads(json_response.read())
			if not data["STATUS"]==200:
				self.error = data["MESSAGE"]
				global_error = self.error
				return data["MESSAGE"]

			self.machine_ip = data["MESSAGE"]
			self.machine_url = self.base_url + "/pi/" + self.machine_ip +"/pi/experiment/"

			req = self.urllib2.Request(self.machine_url + "initiate", input_data)
			br = urllib2.urlopen(req)

			data = json.loads(br.read())
			if data["STATUS"] == 1:
				self.username = username
				if not os.path.exists(self.logdir):
					os.makedirs(self.logdir)
				logdir = os.path.join(self.logdir, username)
				if not os.path.exists(logdir):
					os.makedirs(logdir)

				self.logfile_handler = open(os.path.join(logdir, data["MESSAGE"]), "a")
				self.status = True
				self.app.execute_javascript("document.getElementById('logfile').innerHTML='" + data["MESSAGE"] + "'")
				f = open(self.scilabreadfname, 'w')
				f.close()
				f = open(self.scilabwritefname, 'w')
				f.close()
				global global_error
				global_error = ""
				return "TRUE"
			else:
				self.error = data["MESSAGE"]
				global_error = self.error
				return data["MESSAGE"]
		except Exception:
			logging.exception("Error in authentication")
			self.error = "Cannot connect to SBHS server."
			global global_error
			global_error = self.error
			return self.error

	@attach(result=str)
	def get_data(self):
		return json.dumps({
			"iter": global_iter,
			"heat": global_cur_heat,
			"fan": global_cur_fan,
			"temp": global_cur_temp,
			"time": global_remaining_time,
			"error": global_error
		})

	def experiment(self):
		while self.status == False:
			time.sleep(0.2)
		try:
			scilabreadf = file(self.scilabreadfname, 'w')
			scilabwritef = file(self.scilabwritefname, 'r')
			logf = self.logfile_handler

			self.scilabreadf = scilabreadf
			self.scilabwritef = scilabwritef

			scilabreadf.flush()
		except Exception:
			logging.exception("Error in experiment files.")
			self.error = 'Failed to access files needed for experiment'
			global global_error
			global_error = self.error
			return False


		while True:
			# read data from file that scilab writes to
			retry_read = True
			while retry_read:
				time.sleep(0.001)
				cur_scilabwrite_pos = scilabwritef.tell()
				scilabwritestr = scilabwritef.readline()
				if not scilabwritestr.endswith('\n'):
					scilabwritef.seek(cur_scilabwrite_pos)
					retry_read = True
				else:
					retry_read = False
			scilabwritestr = scilabwritestr.strip()

			if scilabwritestr != "":
				try:
					scilabwritedata = scilabwritestr.split(' ', 3)
					cur_iter = int(float(scilabwritedata[0]))
					cur_heat = int(float(scilabwritedata[1]))
					cur_fan = int(float(scilabwritedata[2]))
					if (cur_heat > 100):
						cur_heat = 100
					elif (cur_heat < 0):
						cur_heat = 0
					if (cur_fan > 100):
						cur_fan = 100
					elif (cur_fan < 0):
						cur_fan = 0
					cur_variables = ''.join(scilabwritedata[3:]) # converting variable arguments list to string
					cur_time = int(time.time() * 1000)

					self.cur_heat = cur_heat
					self.cur_fan = cur_fan
					self.iter = cur_iter
				except Exception:
					logging.exception("Error in reading data.")
					self.error = 'Invalid data format in ' + self.scilabwritefname + '.'
					global global_error
					global_error = self.error
					return False
			else:
				continue

			# read data from server
			srv_data = False
			while not srv_data:
				try:
					url_com = self.machine_url + 'experiment'
					postdata = urllib.urlencode({
						'iteration' : cur_iter,
						'heat' : cur_heat,
						'fan' : cur_fan,
						'variables' : cur_variables,
						'timestamp' : cur_time
					})
					req = self.urllib2.Request(url_com)
					res = self.urllib2.urlopen(req, postdata)
					content = res.read()
					srv_data = True
					content = json.loads(content)
					# print content
					# check if content is received properly
					if content["STATUS"] == 1:
						data_str = content["MESSAGE"]
						data = data_str.split(",")
						data_str = data[0]
						data_str += ' %d' % int(time.time() * 1000) # add client received time stamp
						# if variable arguments present in server response append it
						if data[1] != "":
							data_str += ' ' + data[1]
						# calculating and printing time remaining in minutes
						self.remaining_time = data[2]
						# write data to file
						scilabreadf.write(data_str + '\n')
						scilabreadf.flush()
						templist = data_str.split(" ")
						self.cur_temp = templist[3]
						# write data to log
						logf.write(data_str + '\n')
						logf.flush()

						global global_cur_heat, global_cur_fan, global_cur_temp
						global global_iter, global_remaining_time, global_error
						global_cur_heat = self.cur_heat
						global_cur_fan = self.cur_fan
						global_cur_temp = self.cur_temp
						global_iter = self.iter
						global_remaining_time = self.remaining_time
						global_error = ""
					else:
						self.error = content["MESSAGE"]
						global global_error
						global_error = self.error
						self.status = False
						return False
				except Exception:
					logging.exception("Error in communicating data to server")
					self.error = "Failed to connect to SBHS. Retrying....."
					global global_error
					global_error = self.error
					time.sleep(0.1)
					srv_data = False

	def run(self):
		self.app.setTemplate("index.html")
		t2 = Thread(target=self.experiment)
		t2.setDaemon(True)
		t2.start()

		self.app.window.resize(self.app.width, self.app.height)
		self.app.window.move(self.app.x_pos, self.app.y_pos)
		self.app.window.show()

		def runner():
			self.app.app.exec_()
			try:
				self.reset()
				self.logfile_handler.close()
				self.scilabreadf.close()
				self.scilabwritef.close()
			except Exception:
				logging.exception("Error while reseting SBHS.")
				pass

		import sys
		sys.exit(runner())
	def reset(self):
		print self.machine_url + "reset"
		self.urllib2.urlopen(self.machine_url + "reset")

if __name__ == "__main__":
	s = SBHSClient()
	s.app.register(s)
	s.run()
