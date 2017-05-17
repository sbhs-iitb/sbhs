from django.shortcuts import render, redirect
from sbhs_server.tables.models import Account
from django.contrib import messages
from sbhs_server.helpers import simple_encrypt
from pages.views import index as INDEX_PAGE
import datetime

# Create your views here.

def new(req):
    return render(req, 'password/new.html')

def password_token(username):
    return simple_encrypt.encrypt(username + ",,," + str(datetime.datetime.now()))

def email(req):
    email = req.POST.get("email")

    account = Account.objects.filter(email=email)

    if len(account) == 1:
        account[0].send_password_link(password_token(account[0].username))
        messages.add_message(req, messages.SUCCESS, "Password reset link has been sent to your email address.")
        return redirect(INDEX_PAGE)

def validate_token(req, token):
    try:
        data = simple_encrypt.decrypt(token)
    except:
        messages.add_message(req, messages.ERROR, "Invalid link")
        return redirect(INDEX_PAGE), False

    data = data.split(",,,")
    if len(data) != 2:
        messages.add_message(req, messages.ERROR, "Invalid link")
        return redirect(INDEX_PAGE), False

    return data, True

def edit(req, token):
    data, flag = validate_token(req, token)
    if not flag:
        return data

    timediff = datetime.datetime.now() - datetime.datetime.strptime(data[1], "%Y-%m-%d %H:%M:%S.%f")

    if timediff.total_seconds() < 7200:
        return render(req, "password/edit.html", {"token": token})
    else:
        messages.add_message(req, messages.ERROR, "The reset link is expired.")
        return redirect(INDEX_PAGE)

def update(req, token):
    data, flag = validate_token(req, token)
    if not flag:
        return data

    timediff = datetime.datetime.now() - datetime.datetime.strptime(data[1], "%Y-%m-%d %H:%M:%S.%f")

    if timediff.total_seconds() < 7200:
        username = data[0]
        account = Account.objects.filter(username=username)
        if len(account) == 1:
            error = ""
            if req.POST.get("email") != account[0].email:
                error = "Invalid email"
            if req.POST.get("password") != req.POST.get("confirm"):
                error = "Passwords do not match"

            if error != "":
                messages.add_message(req, messages.ERROR, error)
                return redirect(INDEX_PAGE)

            account[0].set_password(req.POST.get("password"))
            account[0].save()
            messages.add_message(req, messages.SUCCESS, "Password changed successfully")
            return redirect(INDEX_PAGE)
        else:
            messages.add_message(req, messages.ERROR, "Invalid link")
            return redirect(INDEX_PAGE)
    else:
        messages.add_message(req, messages.ERROR, "The reset link is expired.")
        return redirect(INDEX_PAGE)