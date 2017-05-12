#Dev /KoDe

import datetime
import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sbhs_server.settings") # To make a Django Environment.
from sbhs_server.tables.models import Board
from sbhs_server.sbhs import Sbhs
offline_mid = Board.objects.filter(online=False).values_list("mid", flat = True)
s = Sbhs()
for mid in offline_mid:
    i = 1
    while i<5:
        print "{0} trying mid {1} to reconnect".format(i,mid)
        s.connect(mid)
	i+=1
    print "could not connect"
