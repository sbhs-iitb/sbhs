#!/usb/bin/python
import sbhs
import os
import sys

"""erase the old map_machine_ids.txt file"""
try:
    file('map_machine_ids.txt', 'w').close()
except:
    print 'Failed to create machine map file file'
    sys.exit(1)

"""open the map_machine_ids file for writing"""
try:
    map_machine_file = file('map_machine_ids.txt', 'w')
except:
    print 'Failed to create machine map file file'
    sys.exit(1)

""" get list of device file names that start with ttyUSB* in the /dev folder
    device_files = []"""
device_files = [each for each in os.listdir('/dev') if each.startswith('ttyUSB')]

"""if no device filename found then exit"""
if not device_files:
    print 'No USB device found in /dev folder'
    sys.exit(1)

for device in device_files:
    port_counter = 0
    mid_counter = 0
    s = sbhs.Sbhs()
    # getting the number from the device filename
    dev_id = device[6:]
    print dev_id
    try:
        dev_id = int(dev_id)
    except:
        #res = False
        print 'Invalid device name /dev/%s' % device
        continue
    # connect to device
    res = s.connect_device(dev_id)
    #print res
    if not res:
        print "Couldn't connect to the device on /dev/ttyUSB{0}. Retrying!!".format(dev_id)
        for i in range(5):
            res2 = s.connect_device(dev_id)
            print "Trying!!! Attempt {0} for ttyUSB{1}".format(i, dev_id)
            if res2 == True:
                port_counter += 1
        if port_counter < 3: 
            print 'Cannot connect to /dev/%s.' % device
            s.disconnect()
        
    for ii in range(1,6):
        try:
            machine_id = s.getMachineId()
            print machine_id
        except AttributeError:
            machine_id = -1
        #machine_id = s.getMachineId()
        if machine_id > 0:
            mid_counter+=1
            
    if mid_counter < 3:
        print 'Cannot get machine id from /dev/%s' % device
        s.disconnect()
        continue
    else:
        print 'Found SBHS device /dev/%s with machine id %d' % (device, machine_id)
        map_str = "%d=/dev/%s\n" % (machine_id, device)
        map_machine_file.write(map_str)


print 'Done. Exiting...'
map_machine_file.close()
sys.exit(1)







