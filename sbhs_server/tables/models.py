from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from undelete.models import TrashableMixin
import random, datetime, os
from sbhs_server.helpers import mailer, simple_encrypt
from django.contrib.auth.models import UserManager
from sbhs_server import settings
from django.core.exceptions import ObjectDoesNotExist
#from yaksh.models import Profile
# Create your models here.

class Board(TrashableMixin):

    mid                 = models.IntegerField(unique=True)
    online              = models.BooleanField(default=True)
    temp_offline        = models.BooleanField(default=False)

    created_at          = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at          = models.DateTimeField(auto_now=True, editable=False)

    @staticmethod
    def can_do_random_allotment():
        return not os.path.exists(os.path.join(settings.BASE_DIR, "WORKSHOP_MODE"))

    @staticmethod
    def toggle_random_allotment():
        if Board.can_do_random_allotment():
            f = open(os.path.join(settings.BASE_DIR, "WORKSHOP_MODE"), "w")
            f.close()
        else:
            os.remove(os.path.join(settings.BASE_DIR, "WORKSHOP_MODE"))

    @staticmethod
    def allot_board():
        if Board.can_do_random_allotment():
            online_boards_count = len(settings.online_mids)
            board_num = random.randrange(online_boards_count)
            return settings.online_mids[board_num]
        else:
            online_boards = sorted(settings.online_mids)

            # When the account table is empty, allocate first board 
            try:
                last_allocated_MID = Account.objects.select_related().order_by("-id")[0].board.mid;
                for o in online_boards:
                    if o > last_allocated_MID:
                        return Board.objects.get(mid=o).id
            except ObjectDoesNotExist:
                pass
            
            # check if there is at least one online board
            try:
                return Board.objects.get(mid=online_boards[0]).id    
            except Exception as e:
                return -1    

    def image_link(self):
        return settings.WEBCAM_STATIC_DIR + "image" + str(self.mid) + ".jpeg"


class Account(TrashableMixin, AbstractBaseUser):

    name                = models.CharField(max_length=255)
    username            = models.CharField(max_length=127, unique=True)
    email               = models.EmailField(max_length=255, unique=True)
    # password = models.CharField(max_length=255) # Already covered in AbstractBaseUser

    is_active           = models.BooleanField(default=False)
    is_admin            = models.BooleanField(default=False)
    board               = models.ForeignKey("Board")

    created_at          = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at          = models.DateTimeField(auto_now=True, editable=False)

    objects = UserManager()

    USERNAME_FIELD = "username"

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    def send_confirmation(self):
        message = """Hi,\n\nPlease visit the link """ + settings.BASE_URL +  """sbhs/account/confirm/"""
        message = message + self.confirmation_token()
        message = message + """ to confirm your account.\n\n\nRegards,\nVlabs Team"""
        mailer.email(self.email, "Please confirm your account", message)

    def send_password_link(self, token):
        message = """Hi,\n\nPlease visit the link """ + settings.BASE_URL +  """password/edit/"""
        message = message + token
        message = message + """ to change your password.\n\n\nRegards,\nVlabs Team"""
        mailer.email(self.email, "SBHS vlabs password reset link", message)

    def get_profile(self):
        return self.profile


    def confirmation_token(self):
        return simple_encrypt.encrypt(self.email)


class Slot(TrashableMixin):

    start_hour          = models.IntegerField()
    start_minute        = models.IntegerField()

    end_hour            = models.IntegerField()
    end_minute          = models.IntegerField()

    created_at          = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at          = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        sh = str(self.start_hour) if len(str(self.start_hour)) == 2 else "0" + str(self.start_hour)
        sm = str(self.start_minute) if len(str(self.start_minute)) == 2 else "0" + str(self.start_minute)
        eh = str(self.end_hour) if len(str(self.end_hour)) == 2 else "0" + str(self.end_hour)
        em = str(self.end_minute) if len(str(self.end_minute)) == 2 else "0" + str(self.end_minute)
        return sh + ":" + sm + " -- " + eh + ":" + em

    @staticmethod
    def indices(self, other):
        # These lines are irrelevant due to booking date scheme
        #
        # now = datetime.datetime.now()
        # cur_hour = now.hour

        # s = abs(cur_hour - self.start_hour)
        # s = s + 100 if self.start_hour < cur_hour else s
        # o = abs(cur_hour - other.start_hour)
        # o = o + 100 if other.start_hour < cur_hour else o
        return self.start_hour, other.start_hour

    def __lt__(self, other):
        s, o = Slot.indices(self, other)
        return s < o

    def __gt__(self, other):
        s, o = Slot.indices(self, other)
        return s > o

    def __ne__(self, other):
        s, o = Slot.indices(self, other)
        return s != o

    def __eq__(self, other):
        s, o = Slot.indices(self, other)
        return s == o

    def __le__(self, other):
        s, o = Slot.indices(self, other)
        return s <= o

    def __ge__(self, other):
        s, o = Slot.indices(self, other)
        return s >= o

    @staticmethod
    def current_slots(mid):
        now = datetime.datetime.now()
        slots = list(Slot.objects.filter(start_hour=now.hour, end_minute__gt=now.minute))
        bookings = Booking.objects.filter(booking_date__year=now.year,
                                            booking_date__month=now.month,
                                            booking_date__day=now.day, slot__in=slots,
                                            account__board__mid=mid)
        for b in bookings:
            if b.slot in slots:
                slots.remove(b.slot)

        return slots

    @staticmethod
    def slots_now():
        now = datetime.datetime.now()
        slots = list(Slot.objects.filter(start_hour=now.hour))
        return slots

    @staticmethod
    def get_free_slots(mid):
        now = datetime.datetime.now()
        slots = list(Slot.objects.filter(start_hour__gte=now.hour))
        bookings = Booking.objects.filter(booking_date__year=now.year,
                                            booking_date__month=now.month,
                                            booking_date__day=now.day, slot__in=slots,
                                            account__board__mid=mid)
        for b in bookings:
            if b.slot in slots:
                slots.remove(b.slot)

        return sorted(slots)

    @staticmethod
    def get_free_slots_on(date, mid):
        now = datetime.datetime.now()
        if date.strftime("%Y-%m-%d") == now.strftime("%Y-%m-%d"):
            slots = list(Slot.get_free_slots(mid))
        elif date > now:
            slots = list(Slot.objects.all())
            bookings = Booking.objects.filter(booking_date__year=date.year,
                                                booking_date__month=date.month,
                                                booking_date__day=date.day,
                                                account__board__mid=mid)

            for b in bookings:
                if b.slot in slots:
                    slots.remove(b.slot)
        else:
            slots = []

        return sorted(slots)


class Booking(TrashableMixin):

    account             = models.ForeignKey("Account")
    slot                = models.ForeignKey("Slot")

    booking_date        = models.DateTimeField()

    created_at          = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at          = models.DateTimeField(auto_now=True, editable=False)

    def start_time(self):
        return self.booking_date.replace(hour=self.slot.start_hour, minute=self.slot.start_minute)

    def end_time(self):
        return self.booking_date.replace(hour=self.slot.end_hour, minute=self.slot.end_minute)


class Experiment(TrashableMixin):

    booking             = models.ForeignKey("Booking")

    log                 = models.CharField(max_length=255)
    checksum            = models.CharField(max_length=255, default="NONE")

    created_at          = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at          = models.DateTimeField(auto_now=True, editable=False)
