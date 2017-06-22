from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import login as LOGIN
from sbhs_server.tables.models import Slot, Account, Experiment, Booking
import json, datetime, os, time
from django.views.decorators.csrf import csrf_exempt
from sbhs_server import settings
# Create your views here.
# 
def check_connection(req):
    """ Checks if the connection exists or not.
        Input: req:request object.
        Output: HttpResponse object.
    """
    return HttpResponse("TESTOK")

@csrf_exempt
def initial_login(req):
    """ Logs in an user for conducting the experiment on the specified board.
        Input: req:request object.
        Output: HttpResponse object.
    """
    username = req.POST.get("username")
    rpi_ip = ''
    try:
        assigned_mid = Account.objects.select_related().get(username=username).board.mid
    except Exception as e:
        return HttpResponse(json.dumps({"STATUS": 400, "MESSAGE": {"IS_IP":"1","DATA":"Invalid username"}}))
            
    rpi_ip = settings.pi_ip_map[str(assigned_mid)]

    return HttpResponse(json.dumps({"STATUS": 200, "MESSAGE": {"IS_IP":"1","DATA":rpi_ip}}))
#    return HttpResponse(key)
# @login_required(redirect_field_name=None)
@csrf_exempt
def experiment(req):
    """ Manages an ongoing experiment.
        Alert the user when:
            The slot has ended.
            The slot wasn't booked.
        Input: req:request object.
        Output: HttpResponse object.
    """
    try:
        server_start_ts = int(time.time() * 1000)
        from sbhs_server.settings import boards
        user = req.user
        key = str(user.board.mid)
        experiment = Experiment.objects.select_related().filter(id=boards[key]["experiment_id"])

        if len(experiment) == 1 and user.id == experiment[0].booking.account.id and experiment[0].booking.trashed_at == None:
            experiment = experiment[0]
            now = datetime.datetime.now()
            endtime = experiment.booking.end_time()
            if endtime > now:
                timeleft = int((endtime-now).seconds)
                heat = max(min(int(req.POST.get("heat")), 100), 0)
                fan = max(min(int(req.POST.get("fan")), 100), 0)

                boards[key]["board"].setHeat(heat)
                boards[key]["board"].setFan(fan)
                temperature = boards[key]["board"].getTemp()
                log_data(boards[key]["board"], key, experiment.id, heat=heat, fan=fan, temp=temperature)

                server_end_ts = int(time.time() * 1000)

                STATUS = 1
                MESSAGE = "%s %d %d %2.2f" % (req.POST.get("iteration"),
                                            heat,
                                            fan,
                                            temperature)
                MESSAGE = "%s %s %d %d,%s,%d" % (MESSAGE,
                                            req.POST.get("timestamp"),
                                            server_start_ts,
                                            server_end_ts,
                                            req.POST.get("variables"), timeleft)

                f = open(experiment.log, "a")
                f.write(" ".join(MESSAGE.split(",")[:2]) + "\n")
                f.close()
            else:
                # boards[key]["board"].setHeat(0)
                # boards[key]["board"].setFan(100)
                # log_data(boards[key]["board"], key)
                reset(req)
                
                STATUS = 0
                MESSAGE = "Slot has ended. Please book the next slot to continue the experiment."

                reset(req)
                boards[key]["experiment_id"] = None
        else:
            STATUS = 0
            MESSAGE = "You haven't booked this slot."

        return HttpResponse(json.dumps({"STATUS": STATUS, "MESSAGE": MESSAGE}))
    except Exception:
        return HttpResponse(json.dumps({"STATUS": 0, "MESSAGE": "Invalid input. Perhaps the slot has ended. Please book the next slot to continue the experiment."}))

@csrf_exempt
def reset(req):
    """ Resets an experiment.
        Input: req:request object.
        Output: HttpResponse object.
    """
    try:
        from sbhs_server.settings import boards
        user = req.user
        if user.is_authenticated():
            key = str(user.board.mid)
            experiment = Experiment.objects.select_related().filter(id=boards[key]["experiment_id"])

            if len(experiment) == 1 and user == experiment[0].booking.account:
                experiment = experiment[0]
                now = datetime.datetime.now()
                endtime = experiment.booking.end_time()

                boards[key]["board"].setHeat(0)
                boards[key]["board"].setFan(100)

                log_data(boards[key]["board"], key, experiment.id, 0, 100)
                if endtime < now:
                    boards[key]["experiment_id"] = None
    except:
        pass

    return HttpResponse("")

def client_version(req):
    """ Input: req:request object.
        Output: HttpResponse object.
    """
    return HttpResponse("3")

@login_required(redirect_field_name=None)
    
def logs(req):
    """ Renders experimental log files to the user interface.
        Input: req:request object.
        Output: HttpResponse object.
    """
    bookings         = Booking.objects.only("id").filter(account__id=req.user.id)
    deleted_bookings = Booking.trash.only("id").filter(account__id=req.user.id)
    bookings = list(bookings) + list(deleted_bookings)
    booking_ids = [b.id for b in bookings]
    experiments = Experiment.objects.select_related("booking", "booking__slot").filter(booking_id__in=booking_ids)
    for e in experiments:
        e.logname = e.log.split("/")[-1]
    return render(req, "experiment/logs.html", {"experiments": reversed(experiments)})

@login_required(redirect_field_name=None)
def download_log(req, experiment_id, fn):
    """ Downloads the experimental log file.
        Input: req: request object, experiment_id: experimental id, fn: filename.
        Output: HttpResponse object
    """
    try:
        experiment_data = Experiment.objects.select_related("booking", "booking__account").get(id=experiment_id)
        assert req.user.id == experiment_data.booking.account.id
        f = open(experiment_data.log, "r")
        data = f.read()
        f.close()
        return HttpResponse(data, content_type='text/text')
    except:
        return HttpResponse("Requested log file doesn't exist.")

def log_data(sbhs, mid, experiment_id, heat=None, fan=None, temp=None):
    """ Update the experimental log file.
        Input: sbhs:board object, mid: machine-id of the SBHS, experiment_id: experimental id, heat: heater value, fan: fan value, temp: temperature.
    """
    if heat is None:
        heat = sbhs.getHeat()
    if fan is None:
        fan = sbhs.getFan()
    if temp is None:
        temp = sbhs.getTemp()

    data = "%f %s %s %s\n" % (time.time(), str(heat), str(fan), str(temp))
    experiment_logfile = Experiment.objects.get(id=experiment_id).log
    global_logfile = settings.SBHS_GLOBAL_LOG_DIR + "/" + str(mid) + ".log"
    with open(global_logfile, "a") as global_loghandler, open(experiment_logfile, "a") as experiment_loghandler:
        global_loghandler.write(data)
        experiment_loghandler.write(data) 

def validate_log_file(req):
    """ Validates the experimental log file.
        Input: req: request object.
        Output: HttpResponse object.
    """
    import hashlib
    data = req.POST.get("data")
    data = data.strip().split("\n")
    clean_data = ""
    for line in data:
        columns = line.split(" ")
        if len(columns) >= 6:
            clean_data += (" ".join(columns[0:6]) + "\n")

    checksum = hashlib.sha1(clean_data).hexdigest()

    try:
        e = Experiment.objects.get(checksum=checksum)
        return HttpResponse("TRUE")
    except:
        return HttpResponse("FALSE")
