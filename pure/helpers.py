from django.core.mail import send_mail
from django.conf import settings


def send_forget_password_token(email, token):
    subject = 'Your foget password link'
    message = f'''
    Hi,

We hope this email finds you well. We're writing to let you know that you recently signed up for an account on Pure Earth, the online platform that connects individuals and organizations with sustainability initiatives around the world.

To complete your profile and start making a positive impact, we need to verify your email address. This is a quick and easy step that helps us ensure that you are who you say you are.

Please click on the link below to verify your Pure Earth profile:

https://thepureearth.com/reset-password/{token}

If you did not sign up for an account on Pure Earth, please ignore this email and your account will not be created.

We're excited to have you on board and can't wait to see the positive impact you will make in the world!

Best regards,

The Pure Earth Team'''
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return True


def send_username(email, username):
    subject = 'Your The Pure Earth account username'
    message = f'Hi, your The Pure Earth account username is {username}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return True
