import urllib2

proxy_handler = urllib2.ProxyHandler({})
opener = urllib2.build_opener(proxy_handler)
page = opener.open('http://vlabs.iitb.ac.in/sbhs/', timeout=20)
