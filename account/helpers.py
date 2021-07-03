from django.core.mail import send_mail
import uuid
from django.conf import settings
import os
def forget_password_mail(email,token):
    subject='Your forget password link '
    print(token)
    messages = f'click on link to reset password http://127.0.0.1:8000/account/change_password/{token}/'
    email_from = settings.EMAIL_HOST_USER
    recipient =['kitfood101@gmail.com']
    send_mail(subject,messages,email_from,recipient)
    return True

