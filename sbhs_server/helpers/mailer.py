from sbhs_server import settings
import smtplib

def email(to, subject, message):
    smtpserver = smtplib.SMTP()
    smtpserver.connect(settings.EMAIL_HOST, settings.EMAIL_PORT)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo()
    smtpserver.esmtp_features['auth']='LOGIN DIGEST-MD5 PLAIN'
    smtpserver.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

    header = 'To: ' + to + '\n' + 'From: ' + settings.EMAIL_HOST_USER + '@iitb.ac.in\n' + 'Subject: ' + subject +' \n'
    msg = header + '\n' + message + '\n\n'
    smtpserver.sendmail(settings.EMAIL_HOST_USER + '@iitb.ac.in', to, msg)
    smtpserver.close()