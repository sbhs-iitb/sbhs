import os, serial, smtplib
from time import sleep
from sbhs_server.credentials import ADMIN_EMAIL
from sbhs_server.helpers import mailer 

#Setting default device parameters
MAX_PORTS = 256
MIN_TEMP = 10
MAX_TEMP = 70

def write_to_port(s, com, arg):
    """ Sets fan/heater value based on input command code and entered parameter.
        Inputs: s:serial port object, com: number that distinguishes commands, arg: value to be set for that parameter.
    """
    s.write(chr(int(com)))
    sleep(0.5)
    s.write(chr(int(arg)))
    sleep(0.5)

def read_from_port(s, com):
    """ Reads mid/temperature based on input command code.
        Inputs: s:serial port object, com: number that distinguishes commands.
        Output: result: temperature if com=255, mid if com=252, and -1 in case of invalid command code.
    """
    s.write(chr(int(com)))
    sleep(0.5)
    if com == 255:
        result = ord(s.read(1)) + (0.1 * ord(s.read(1)))
    elif com == 252:
        result = ord(s.read(1))
    else:
        result = -1
    sleep(0.5)
    return result

def create_message(check_mids, defective_ports):
    """ Creates message to be sent to the admin for monitoring ports and devices.
        Inputs: check_mids: list of mids for devices to be checked, defective_ports: list of defective ports.
        Output: msg: message with list of mids of devices to be checked and defective ports that is to be mailed to the admin.
    """
    msg = ''
    if len(check_mids) != 0:
        msg += 'Please check the following machine ids :\n'
        for i,mid in enumerate(check_mids):
            msg = msg + str(i) + '. ' + str(mid) + '\n'
    if len(defective_ports) != 0:
        msg = msg + '\nPlease check the following ports :\n'
        for port in defective_ports:
            msg = msg + str(port) + '\n'
    return msg

def main():
    """ Attempts to open serial port object on existing USB paths, and then read the mid of the device using read_from port() function.
        Sets fan and heater value to 100 and 0 respectively using write_to_port() function,
        and reads the temperature of the same device using read_from port() function.
        if the serial port opens but the mid returned is less than zero
            append it to the list of defective ports.
        if an exception occurs while reading or writing but the port opens successfully and returns a valid mid
            then add it to the list of offline mids.
        if the ports opens successfully, returns a valid mid and temperature, and encounters no exceptions
            then add it to the list of present_online_mids
        The difference between the sets of online_mids and present_online_mids gives the list of mids of devices to be checked.
        Calls the create_message function and mails the returned message to the admin.
    """
    present_online_mids, offline_mids, defective_ports = [], [], []
    for i in range(0,MAX_PORTS):
        path = '/dev/ttyUSB' + str(i)
        if os.path.exists(path):
            try:
                s = serial.Serial(port=path, baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=2)
                if not s.is_open:
                    s.open()
                assert s.is_open
                mid = read_from_port(s, 252) # get machine id
                assert mid > 0
                write_to_port(s, 253, 100) # set fan speed
                write_to_port(s, 254, 0) # set heater value
                current_temp = read_from_port(s, 255) # get current temperature
                assert current_temp >= MIN_TEMP and current_temp <= MAX_TEMP
                present_online_mids.append(mid)
            except:
                if s.is_open:
                    if mid > 0:
                        offline_mids.append(mid)
                    else:
                        defective_ports.append(path)
            if s.is_open:
                s.close()
    check_mids = list(set(online_mids).difference(set(present_online_mids)))
    msg = create_message(check_mids, defective_ports)
    if len(msg) == 0:
        msg = "Nothing out of order was detected on the server. :)"
    #thread.start_new_thread(mailer.email, (ADMIN_EMAIL, "Health report of SBHS Server", msg))
    mailer.email(ADMIN_EMAIL, "Health report of SBHS Server", msg)
    #print msg

if __name__ == "__main__":
    main()




