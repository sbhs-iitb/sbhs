import json

pi_ip_map = {}
ipaddrs = []

with open("temp/ipaddrs.txt", "r") as filehandler:
	ipaddrs = filehandler.readlines()

ipaddrs = [ip.strip() for ip in ipaddrs]

for ip in ipaddrs:
	filename = "temp/" + ip + ".txt"
	with open(filename, "r") as filehandler:
		for line in filehandler:
			try:
				data = line.split('=')
				pi_ip_map[data[0].strip()] = ip
			except:
				pass
				
json_data = json.dumps(pi_ip_map, indent=2, separators=(',',':'))
with open("pi-ip.json", "w") as filehandler:
	filehandler.write(json_data)