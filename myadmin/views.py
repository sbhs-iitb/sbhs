from django.shortcuts import render, redirect
from django.http import Http404,HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count
from django.db import connection
from django.core.exceptions import ObjectDoesNotExist
from sbhs_server.tables.models import Board, Booking, Slot, Experiment, Account
from sbhs_server import settings,sbhs
import subprocess,json,serial,os, datetime
# Create your views here.

def checkadmin(req):
    """ Checks for valid admin
            Raises Http error if:
                Requested user is not admin.
        Input: s: request object.
        Output: HttpResponse      
    """
    if not req.user.is_admin:
        raise Http404

@login_required(redirect_field_name=None)
def index(req):
    checkadmin(req)
    boards = Board.objects.order_by('-online').all()
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
    bookings = Booking.objects.order_by('-booking_date','-slot_id').filter(trashed_at__isnull=True).select_related()[:50]
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
    now = datetime.datetime.now()
    current_slot_id = Slot.objects.filter(start_hour=now.hour,
                                            start_minute__lt=now.minute,
                                            end_minute__gt=now.minute)

    current_slot_id = -1 if not current_slot_id else current_slot_id[0].id

    current_bookings = Booking.objects.filter(slot_id=current_slot_id,
                                                booking_date=datetime.date.today()).select_related()
    current_mids = list([-1]) if not current_bookings else [current_booking.account.board.mid for current_booking in current_bookings]

    boards = Board.objects.filter(online=1)
    allotment_mode = "Random" if Board.can_do_random_allotment() else "Workshop"
    return render(req, 'admin/testexp.html', {"boards": boards, "allotment_mode": allotment_mode, "mids": current_mids})

@csrf_exempt
def monitor_experiment(req):
    checkadmin(req)
    try:
        mid = int(req.POST.get("mid"))
    except Exception as e:
        return HttpResponse(json.dumps({"status_code":400, "message":"Invalid parameters"}), content_type="application/json")

    now = datetime.datetime.now()
    current_slot_id = Slot.objects.filter(start_hour=now.hour,
                                            start_minute__lt=now.minute,
                                            end_minute__gt=now.minute)

    current_slot_id = -1 if not current_slot_id else current_slot_id[0].id

    try:
        current_booking = Booking.objects.get(slot_id=current_slot_id,
                                                    booking_date=datetime.date.today(),
                                                    account__board__mid=mid)
    except Exception as e:
        return HttpResponse(json.dumps({"status_code":400, "message":"Invalid MID"}), content_type="application/json")

    try:
        current_booking_id, current_user = current_booking.id, current_booking.account.username

        logfile = Experiment.objects.filter(booking_id=current_booking_id).order_by('created_at').reverse()[0].log
    except:
        return HttpResponse(json.dumps({"status_code":417, "message": "Experiment hasn't started"}), content_type="application/json")

    try:
        # get last 10 lines from logs
        stdin,stdout = os.popen2("tail -n 10 "+logfile)
        stdin.close()
        logs = stdout.readlines(); stdout.close()
        screened_logs = []
        for line in logs:
            screened_line = " ".join(line.split()[:4]) + "\n"
            screened_logs.append(screened_line)

        logs = "".join(screened_logs)
    except Exception as e:
        return HttpResponse(json.dumps({"status_code":500, "message":str(e)}), content_type="application/json")

    data = {"user": current_user, "logs": logs}
    return HttpResponse(json.dumps({"status_code":200, "message":data}), content_type="application/json")

@login_required(redirect_field_name=None)
def get_allocated_mids(req):
    checkadmin(req)
    with connection.cursor() as cursor:
        cursor.execute("SELECT tables_board.mid, COUNT(tables_account.id), tables_board.id FROM tables_account RIGHT OUTER JOIN tables_board ON tables_account.board_id = tables_board.id WHERE tables_board.online = 1 GROUP BY tables_board.mid ORDER BY COUNT(tables_account.id)")
        mid_count = cursor.fetchall()

    return render(req, 'admin/changeMID.html', {"mid_count" : mid_count})

@csrf_exempt
def get_users(req):
    checkadmin(req)
    try:
        users = list(Account.objects.values_list("username", flat=True))
        return HttpResponse(json.dumps({"status_code":200, "message":users}), content_type="application/json")
    except Exception as e:
        return HttpResponse(json.dumps({"status_code":500, "message":str(e)}), content_type="application/json")


@csrf_exempt
def toggle_device_status(req):
    checkadmin(req)

    try : 
        mid = req.POST.get('mid')
    except Exception as e:
        return HttpResponse(json.dumps({"status_code":400, "message":"Invalid parameters"}), content_type="application/json")

    try:
        now = datetime.datetime.now()
        current_slot_id = Slot.objects.filter(start_hour=now.hour,
                                                start_minute__lt=now.minute,
                                                end_minute__gt=now.minute)

        current_slot_id = -1 if not current_slot_id else current_slot_id[0].id

        current_bookings = Booking.objects.filter(slot_id=current_slot_id,
                                                    booking_date=datetime.date.today()).select_related()
        current_mids = list([-1]) if not current_bookings else [current_booking.account.board.mid for current_booking in current_bookings]
    except Exception as e:
        return HttpResponse(json.dumps({"status_code":400, "message":"Unsuccessful"}), content_type="application/json")

    if int(mid) in current_mids:
        return HttpResponse(json.dumps({"status_code":400, "message":"Board is in use."}), content_type="application/json")

    try:
        brd = Board.objects.get(mid = mid)
        brd.temp_offline = not brd.temp_offline
        brd.save()

        return HttpResponse(json.dumps({"status_code":200, "message":"Toggle successful"}), content_type="application/json")
    except Exception as e:
        return HttpResponse(json.dumps({"status_code":400, "message":"Unsuccessful"}), content_type="application/json")


def user_exists(username):
    try:
        user = Account.objects.get(username=username)
    except ObjectDoesNotExist:
        return None
    return user

@csrf_exempt
def update_allocated_mid(req):
    checkadmin(req)
    try:
        username = req.POST.get("username")
        board_id = req.POST.get("board_id")
    except Exception as e:
        return HttpResponse(json.dumps({"status_code":400, "message":"Invalid parameters"}), content_type="application/json")

    user = user_exists(username)
    if user is not None:
        user.board_id = board_id
        user.save()
    else:
        return HttpResponse(json.dumps({"status_code": 400, "message": "Username does not exist"}), content_type="application/json")

    return HttpResponse(json.dumps({"status_code": 200, "message": "MID changed successfully"}), content_type="application/json")

@login_required(redirect_field_name=None)
def download_log(req, mid):
    checkadmin(req)
    try:
        global_logfile = settings.SBHS_GLOBAL_LOG_DIR + "/" + mid + ".log"
        f = open(global_logfile, "r")
        data = f.read()
        f.close()
        return HttpResponse(data, content_type='text/text')
    except:
        return HttpResponse("Requested log file doesn't exist.")


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
        return HttpResponse(json.dumps(retVal),content_type='application/json')

    #trying to connect to device

    # check if SBHS device is connected
    if not os.path.exists(usb_path):
        retVal={"status_code":500,"message":"Device Not connected to defined USB Port"}
        return HttpResponse(json.dumps(retVal),content_type='application/json')

    try:
        board = sbhs.Sbhs()
        board.machine_id=mid
        board.boardcon= serial.Serial(port=usb_path, baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=2) #orignal stopbits = 1
        board.status = 1
        if board.reset_board():
            retVal={"status_code":200,"message":board.getTemp()}
            return HttpResponse(json.dumps(retVal),content_type='application/json')
        else:
            retVal={"status_code":500,"message":"Could not set the parameters.Try again."}
            return HttpResponse(json.dumps(retVal),content_type='application/json')
    except serial.serialutil.SerialException:
        retVal={"status_code":500,"message":"Could not connect to the device.Try again."}
        return HttpResponse(json.dumps(retVal),content_type='application/json')


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
        return HttpResponse(json.dumps(retVal),content_type='application/json')

    #trying to connect to device

    # check if SBHS device is connected
    if not os.path.exists(usb_path):
        retVal={"status_code":500,"message":"Device Not connected to defined USB Port"}
        return HttpResponse(json.dumps(retVal),content_type='application/json')

    try:
        board = sbhs.Sbhs()
        board.machine_id=mid
        board.boardcon= serial.Serial(port=usb_path, baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=2) #orignal stopbits = 1
        board.status = 1
        if board.setFan(fan) and board.setHeat(heat):
            retVal={"status_code":200,"message":board.getTemp()}
            return HttpResponse(json.dumps(retVal),content_type='application/json')
        else:
            retVal={"status_code":500,"message":"Could not set the parameters.Try again."}
            return HttpResponse(json.dumps(retVal),content_type='application/json')
    except serial.serialutil.SerialException:
        retVal={"status_code":500,"message":"Could not connect to the device.Try again."}
        return HttpResponse(json.dumps(retVal),content_type='application/json')

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
        return HttpResponse(json.dumps(retVal),content_type='application/json')

    #trying to connect to device

    # check if SBHS device is connected
    if not os.path.exists(usb_path):
        retVal={"status_code":500,"message":"Device Not connected to defined USB Port"}
        return HttpResponse(json.dumps(retVal),content_type='application/json')

    try:
        board = sbhs.Sbhs()
        board.machine_id=mid
        board.boardcon= serial.Serial(port=usb_path, baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=2) #orignal stopbits = 1
        board.status = 1
        temp=board.getTemp()
        if temp!=0.0:
            retVal={"status_code":200,"message":temp}
            return HttpResponse(json.dumps(retVal),content_type='application/json')
        else:
            retVal={"status_code":500,"message":"Could not set the parameters.Try again."}
            return HttpResponse(json.dumps(retVal),content_type='application/json')
    except serial.serialutil.SerialException:
        retVal={"status_code":500,"message":"Could not connect to the device.Try again."}
        return HttpResponse(json.dumps(retVal),content_type='application/json')
