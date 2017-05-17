from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from sbhs_server.tables.models import Account, Slot, Booking
import datetime

LIMIT = 2

@login_required(redirect_field_name=None)
def new(req):
    cur_slots = Slot.current_slots(req.user.board.mid)
    all_slots = Slot.get_free_slots(req.user.board.mid)
    date = (datetime.datetime.now()).strftime("%Y-%m-%d")
    return render(req, "slot/new.html", {"all_slots": all_slots, "cur_slots": cur_slots, "nowdate": date})

@login_required(redirect_field_name=None)
def show(req, date_string):
    date = datetime.datetime.strptime(date_string, "%Y-%m-%d")
    all_slots = Slot.get_free_slots_on(date, req.user.board.mid)
    return render(req, "slot/show.html", {"all_slots": all_slots})

@login_required(redirect_field_name=None)
def create(req):
    slot = Slot.objects.get(id=req.POST.get("slot"))
    date_string = req.POST.get("date")
    date = datetime.date.today() if date_string == "CURRENT" else datetime.datetime.strptime(date_string, "%Y-%m-%d")
    all_slots = Slot.get_free_slots(req.user.board.mid) if date_string == "CURRENT" else Slot.get_free_slots_on(date, req.user.board.mid)

    if slot in all_slots:
        if date_string == "CURRENT":
            Booking.objects.create(slot=slot, account=req.user, booking_date=date)
            messages.add_message(req, messages.SUCCESS, "Slot " + str(slot) + " booked successfully.")
        else:
            bookings = req.user.booking_set.select_related("slot").filter(booking_date__year=date.year,
                                                                        booking_date__month=date.month,
                                                                        booking_date__day=date.day)
            if len(bookings) >= LIMIT:
                messages.add_message(req, messages.ERROR, "Can't book more than " + str(LIMIT) + " slots in a day in advance.")
            elif len(bookings) < LIMIT:
                consecutive_check = True
                for b in bookings:
                    if abs(b.slot.start_hour - slot.start_hour) <= 1:
                        consecutive_check = False
                        break
                if not consecutive_check:
                    messages.add_message(req, messages.ERROR, "Can't book 2 consecutive slots in a day in advance.")
                else:
                    Booking.objects.create(slot=slot, account=req.user, booking_date=date)
                    messages.add_message(req, messages.SUCCESS, "Slot " + str(slot) + " booked successfully.")
    else:
        messages.add_message(req, messages.ERROR, "Slot " + str(slot) + " already booked.")
    
    return redirect(index)

@login_required(redirect_field_name=None)
def index(req):
    bookings = req.user.booking_set.select_related("slot").order_by("booking_date")

    return render(req, "slot/index.html", {"bookings": reversed(bookings),
                                            "now_time": datetime.datetime.now()})


@login_required(redirect_field_name=None)
def delete(req, booking_id):
    try:
        booking = Booking.objects.select_related("slot").get(id=booking_id)
        assert booking.account_id == req.user.id
        if booking.start_time() > datetime.datetime.now():
            booking.delete()
            messages.add_message(req, messages.SUCCESS, "Slot booking deleted successfully.")
        else:
            messages.add_message(req, messages.ERROR, "Slot time is over. Cannot delete this booking now.")
    except:
        messages.add_message(req, messages.ERROR, "Booking does not exist.")
    
    return redirect(index)
