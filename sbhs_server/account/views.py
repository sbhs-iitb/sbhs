from django.shortcuts import render, redirect
from sbhs_server.tables.models import Account, Board
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib import messages
from sbhs_server.helpers import simple_encrypt
from django.contrib.auth import authenticate
from django.contrib.auth import login as LOGIN
from django.contrib.auth import logout as LOGOUT
from django.contrib.auth.decorators import login_required
# Create your views here.

def index(req):
    if req.user.is_authenticated():
        return redirect(home)
    return render(req, "account/index.html")

def new():
    pass

def create(req):
    error = []

    name        = req.POST.get("name").strip()
    email       = req.POST.get("email").strip()
    username    = req.POST.get("username").strip()
    roll_number = req.POST.get("roll_number").strip()
    password    = req.POST.get("password")
    confirm     = req.POST.get("confirm")
    institute   = req.POST.get("institute").strip()
    department  = req.POST.get("department").strip()
    position    = req.POST.get("position").strip()

    error = error + (["Please enter a name."] if name == "" else [])
    error = error + (["Please enter an email."] if email == "" else [])
    error = error + (["Please enter an username."] if username == "" else [])
    error = error + (["Please enter a roll_number."] if roll_number == "" else [])
    
    error = error + (["Please enter a password."] if password == "" else [])
    error = error + (["Password confirmation does not match."] if password != confirm else [])

    error = error + (["Please enter an institute."] if institute == "" else [])
    error = error + (["Please enter a department."] if department == "" else [])
    error = error + (["Please enter a position."] if position == "" else [])

    try:
        validate_email(email)
    except ValidationError:
        error = error + ["Please enter a valid email."]

    email_exists = Account.objects.filter(email=email).count()
    error = error + (["Account with given email already exists."] if email_exists > 0 else [])

    username_exists = Account.objects.filter(username=username).count()
    error = error + (["Account with given username already exists."] if username_exists > 0 else [])

    if error != []:
        messages.add_message(req, messages.ERROR, "<br>".join(error))
        return redirect(index)

    # try:
    account = Account(
                name=name,
                username=username,
                email=email,
                board_id=Board.allot_board()
            )
    account.set_password(password)
    account.save()
    account.send_confirmation()
    print "Done"
    messages.add_message(req, messages.SUCCESS, "You have been registered successfully. Please check your email for confirmation.")
    return redirect(index)
    # except:
    #     messages.add_message(req, messages.ERROR, "Invalid information. Please try again.")
    #     return redirect(index)

def confirm(req, token):
    try:
        email = simple_encrypt.decrypt(token)
        account = Account.objects.get(email=email)
        account.is_active = True
        account.save()
        messages.add_message(req, messages.SUCCESS, "Your email has been confirmed. You can login now.")
    except:
        messages.add_message(req, messages.ERROR, "Invalid confirmation token.")

    return redirect(index)

def login(req):
    username = req.POST.get('username')
    password = req.POST.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            LOGIN(req, user)
            return redirect(index)
        else:
            messages.add_message(req, messages.ERROR, "Your account is not activated yet. Please check your email for activation link.")
            return redirect(index)
    else:
        messages.add_message(req, messages.ERROR, "Invalid username or password.")
        return redirect(index)

def logout(req):
    LOGOUT(req)
    return redirect(index)

@login_required(redirect_field_name=None)
def home(req):
    return render(req, "account/home.html")
