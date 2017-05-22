from django.shortcuts import render, redirect
from django.http import Http404,HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from sbhs_server.tables.models import Board, Booking
from sbhs_server import settings,sbhs
import subprocess,json,serial,os 
# Create your views here.

def checkadmin(req):
    if not req.user.is_admin:
        raise Http404

@login_required(redirect_field_name=None)
def index(req):
    checkadmin(req)
    boards = Board.objects.order_by('online').all()
    allotment_mode = "Random" if Board.can_do_random_allotment() else "Workshop"
    return render(req, 'admin/index.html', {"boards": boards, "allotment_mode": allotment_mode})

@login_required(redirect_field_name=None)
def toggle_allotment_mode(req):
    checkadmin(req)
    Board.toggle_random_allotment()
    return redirect(index)

@login_required(redirect_field_name=None)
def booking_index(req):
    checkadmin(req)
    bookings = Booking.objects.order_by('-booking_date').select_related()[:50]
    return render(req, 'admin/booking_index.html', {"bookings": bookings})

@login_required(redirect_field_name=None)
def webcam_index(req):
    checkadmin(req)
    boards = Board.objects.all()
    return render(req, 'admin/webcam_index.html', {"boards": boards})

@login_required(redirect_field_name=None)
def profile(req, mid):
    checkadmin(req)
    try:
        filename = settings.SBHS_GLOBAL_LOG_DIR + "/" + mid + ".log"
        f = open(filename, "r")
        f.close()
    except:
        raise Http404

    delta_T = 1000
    data = subprocess.check_output("tail -n %d %s" % (delta_T, filename), shell=True)
    data = data.split("\n")
    plot = []
    heatcsv = ""
    fancsv = ""
    tempcsv = ""

    for t in xrange(len(data)):
        line = data[t]
        entry = line.strip().split(" ")
        try:
            plot.append([int(i) for i in entry[0:-1] + [float(entry[-1])]])
            heatcsv += "%d,%s\\n" % (t+1, entry[1])
            fancsv += "%d,%s\\n" % (t+1, entry[2])
            tempcsv += "%d,%s\\n" % (t+1, entry[3])
        except:
            continue

    plot = zip(*plot) # transpose

    return render(req, "admin/profile.html", {
        "mid": mid,
        "delta_T": delta_T,
        "heat": heatcsv,
        "fan": fancsv,
        "temp": tempcsv
    })

@login_required(redirect_field_name=None)
def testing(req):
    checkadmin(req)
    boards = Board.objects.order_by('online').all()
    allotment_mode = "Random" if Board.can_do_random_allotment() else "Workshop"
    return render(req, 'admin/testexp.html', {"boards": boards, "allotment_mode": allotment_mode})

@csrf_exempt
def reset_device(req):
    """Resets the device to fan = 100 and heat = 0
        Takes mid as paramter 
        Returns status_code = 200, data={temp:temp of the device} if succesful
                else 
                status_code = 500 , data={error:errorMessage}
    """ 
    mid=int(req.POST.get('mid'))
    usb_path=settings.MID_PORT_MAP.get(mid,None)

    if usb_path is None:
        retVal={"status_code":400,"message":"Invalid MID"}
        return HttpResponse(json.dumps(retVal))

    #trying to connect to device

    # check if SBHS device is connected
    if not os.path.exists(usb_path):
        retVal={"status_code":500,"message":"Device Not connected to defined USB Port"}
        return HttpResponse(json.dumps(retVal))

    try:
        board = sbhs.Sbhs()
        board.machine_id=mid
        board.boardcon= serial.Serial(port=usb_path, baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=2) #orignal stopbits = 1
        board.status = 1
        if board.reset_board():
            retVal={"status_code":200,"message":board.getTemp()}
            return HttpResponse(json.dumps(retVal))
        else:
            retVal={"status_code":500,"message":"Could not set the parameters.Try again."}
            return HttpResponse(json.dumps(retVal))
    except serial.serialutil.SerialException:
        retVal={"status_code":500,"message":"Could not connect to the device.Try again."}
        return HttpResponse(json.dumps(retVal))


@csrf_exempt
def set_device_params(req):
    """Sets the device parameters as per the arguments sent
        Takes mid,fan,heat as paramter 
        Returns status_code = 200, data={temp:temp of the device} if succesful
                else 
                status_code = 500 , data={error:errorMessage}
    """ 
    mid=int(req.POST.get('mid'))
    fan=int(req.POST.get('fan'))
    heat=int(req.POST.get('heat'))
    usb_path=settings.MID_PORT_MAP.get(mid,None)

    if usb_path is None:
        retVal={"status_code":400,"message":"Invalid MID"}
        return HttpResponse(json.dumps(retVal))

    #trying to connect to device

    # check if SBHS device is connected
    if not os.path.exists(usb_path):
        retVal={"status_code":500,"message":"Device Not connected to defined USB Port"}
        return HttpResponse(json.dumps(retVal))

    try:
        board = sbhs.Sbhs()
        board.machine_id=mid
        board.boardcon= serial.Serial(port=usb_path, baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=2) #orignal stopbits = 1
        board.status = 1
        if board.setFan(fan) and board.setHeat(heat):
            retVal={"status_code":200,"message":board.getTemp()}
            return HttpResponse(json.dumps(retVal))
        else:
            retVal={"status_code":500,"message":"Could not set the parameters.Try again."}
            return HttpResponse(json.dumps(retVal))
    except serial.serialutil.SerialException:
        retVal={"status_code":500,"message":"Could not connect to the device.Try again."}
        return HttpResponse(json.dumps(retVal))

@csrf_exempt
def get_device_temp(req):
    """Sets the device parameters as per the arguments sent
        Takes mid,fan,heat as paramter 
        Returns status_code = 200, data={temp:temp of the device} if succesful
                else 
                status_code = 500 , data={error:errorMessage}
    """ 
    mid=int(req.POST.get('mid'))
    usb_path=settings.MID_PORT_MAP.get(mid,None)

    if usb_path is None:
        retVal={"status_code":400,"message":"Invalid MID"}
        return HttpResponse(json.dumps(retVal))

    #trying to connect to device

    # check if SBHS device is connected
    if not os.path.exists(usb_path):
        retVal={"status_code":500,"message":"Device Not connected to defined USB Port"}
        return HttpResponse(json.dumps(retVal))

    try:
        board = sbhs.Sbhs()
        board.machine_id=mid
        board.boardcon= serial.Serial(port=usb_path, baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=2) #orignal stopbits = 1
        board.status = 1
        temp=board.getTemp()
        if temp!=0.0:
            retVal={"status_code":200,"message":temp}
            return HttpResponse(json.dumps(retVal))
        else:
            retVal={"status_code":500,"message":"Could not set the parameters.Try again."}
            return HttpResponse(json.dumps(retVal))
    except serial.serialutil.SerialException:
        retVal={"status_code":500,"message":"Could not connect to the device.Try again."}
        return HttpResponse(json.dumps(retVal))
