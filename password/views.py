from django.shortcuts import render, redirect
from sbhs_server.tables.models import Account
from django.contrib import messages
from sbhs_server.helpers import simple_encrypt
from pages.views import index as INDEX_PAGE
import datetime

# Create your views here.

def new(req):
    """ Returns html page to set new password
        Input: request object
        Output: renders new.html page through render function.
    """
    return render(req, 'password/new.html')

def password_token(username):
    """ Returns encrypted token
        Input: username
        Output: encrypted token returned by encrypt() function.
    """
    return simple_encrypt.encrypt(username + ",,," + str(datetime.datetime.now()))

def email(req):
    """ Sends the reset password link to the email
            Checks if the user has an account
        Input: request object
        Output: INDEX_PAGE returned by redirect() function.
    """
    email = req.POST.get("email")

    account = Account.objects.filter(email=email)

    if len(account) == 1:
        account[0].send_password_link(password_token(account[0].username))
        messages.add_message(req, messages.SUCCESS, "Password reset link has been sent to your email address.")
        return redirect(INDEX_PAGE)

def validate_token(req, token):
    """ Checks if the token is valid
            Decrypts token and checks for validity
        Input: request object, token.
        Output: INDEX_PAGE returned by redirect() function if Invalid link
                data if Valid link.
    """
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
    """ Allows user to edit the password
            calculates the time and checks if reset link is expired
        Input: request object, token
        Output: renders edit.html page if link is not expired
                shows error message if link is expired and returns the Index_page through redirect()
                function.    
    """
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
    """ Allows user to update the password
            -Checks if token is valid
            -Checks if the link is expired
            -Checks if email entered by user is valid
            -Checks if passwords of password and confirm field matches
        Input: request object , token.
        Output: Message "Password changed successfully" if success
                Message "Invalid link" or "Reset link is expired" if respective validations fails.      
    """
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