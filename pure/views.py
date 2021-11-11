from django.http.response import HttpResponse
from django.shortcuts import render, redirect
import uuid
from .models import *
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .helpers import send_forget_password_token
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

# Create your views here.


# Home page
def home(request):
    return render(request, 'screens/Home.html')


# FAQ page
def faq(request):
    return render(request, 'screens/FAQ.html')


# TNC page
def tnc(request):
    return render(request, 'screens/TNC.html')


# Privacy page
def privacy(request):
    return render(request, 'screens/Privacy.html')


# Shipping page
def shipping(request):
    return render(request, 'screens/Shipping.html')


# Return page
def Return(request):
    return render(request, 'screens/Return.html')


# About page
def about(request):
    return render(request, 'screens/About.html')


# Contact page
def contact(request):
    return render(request, 'screens/Contact.html')


# Profile page
@login_required
def profile(request):
    return render(request, 'dashboard/profile.html')


# error page
def error():
    return HttpResponse('404 - Page Not Found')


 # Login and Signup page

# Signin page
@csrf_exempt
def handleLogin(request):
    if request.method == 'POST':
        loginusername = request.POST['loginusername']
        loginpass = request.POST['loginpass']

        user = authenticate(username=loginusername, password=loginpass)
        user_auth_obj = UserAuth.objects.filter(user=user).first()
        if not user_auth_obj.is_Verified:
            messages.error(request, 'Please verify your account')
            return redirect('/login')
        if user is not None:
            login(request, user)
            messages.success(request, 'You have been logged in successfully')
            return redirect('/')
        else:
            messages.error(request, 'Invalid Credentials! Please Try Again')
            return redirect('/login')

    return render(request, 'registration/login.html')


# SignOut page
def handleLogout(request):
    messages.success(request, 'You have been logged out successfully')
    logout(request)
    return redirect('/')


# SignUp page
@csrf_exempt
def handleSignup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        confpass = request.POST['confpass']

        try:
            if User.objects.filter(username=username).first():
                messages.error(request, 'Username already exists')
                return redirect('/signup')
            if User.objects.filter(email=email).first():
                messages.error(request, 'Email already exists')
                return redirect('/signup')
            if pass1 != confpass:
                messages.error(request, 'Password and Confirm Password does not match')
                return redirect('/signup')
            if len(pass1) < 8:
                messages.error(request, 'Password must be atleast 8 characters')
                return redirect('/signup')
            if len(username) < 6 and not username.isalnum():
                messages.error(request, 'Username must be atleast 8 characters')
                messages.error(request, 'Username should contain only letters and numbers')
                return redirect('/signup')
            auth_token = str(uuid.uuid4())
            user_obj = User.objects.create(username=username, email=email)
            user_obj.set_password(pass1)
            user_obj.save()
            user_auth_obj = UserAuth.objects.create(user=user_obj, auth_token=auth_token)
            user_auth_obj.save()
            messages.success(request, 'Your The Pure Earth account has been successfully created')
            messages.success(request, 'Please check your email for verification')
            activate_account(email, auth_token)
            return redirect('/login')

        except Exception as e:
            print(e)
            messages.error(request, 'Something went wrong')
            return redirect('/signup')
    
    return render(request, 'registration/signup.html')


# activate account function
def activate_account(email, token):
    subject = 'Activate your account'
    message = f'Hi, verify your account: https://pureearth.herokuapp.com/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)


# verification function
def verify(request, auth_token):
    try:
        user_auth_obj = UserAuth.objects.filter(auth_token=auth_token).first()
        if user_auth_obj:
            # check if user is already verified
            if user_auth_obj.is_Verified:
                messages.success(request, 'Account already activated')
                return redirect('/login')
            # if not verified then activate account
            user_auth_obj.is_Verified = True
            user_auth_obj.save()
            messages.success(request, 'Account verified successfully')
            return redirect('/login')
        else:
            messages.success(request, 'Invalid token')
            return redirect('/')
    except Exception as e:
        print(e)


# forget password
def forget_password(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('fusername')
            user_obj = User.objects.filter(username=username).first()
        if user_obj is None:
            messages.error(request, 'No user found')
            return redirect('/forgot-password')
        user_obj = User.objects.get(username=username)
        token = str(uuid.uuid4())
        send_forget_password_token(user_obj.email, token)
        userauth_obj = UserAuth.objects.get(user = user_obj)
        userauth_obj.forget_password_token = token
        userauth_obj.save()
        messages.success(request, 'Reset Password Sent')
        messages.success(request, 'Please check your email for reset password link')
        return redirect('/login')
    except Exception as e:
        print(e)
    return render(request, 'registration/forget.html')


# change password
def change_password(request, token):
    context = {}
    try:
        user_auth_obj = UserAuth.objects.filter(
            forget_password_token=token).first()
        context = {'user_id': user_auth_obj.user.id}
        if request.method == 'POST':
            newpass = request.POST.get('newpass')
            newconfpass = request.POST.get('newconfpass')
            user_id = request.POST.get('user_id')
            if user_id is None:
                messages.error(request, 'No user id found')
                return redirect('/reset-password/{token}')
            if newpass != newconfpass:
                messages.error(request, 'Password does not match')
                return redirect('/reset-password/{token}')
            user_obj = User.objects.get(id=user_id)
            user_obj.set_password(newpass)
            user_obj.save()
            messages.success(request, 'Password changed successfully')
            return redirect('/login')

    except Exception as e:
        print(e)

    return render(request, 'registration/change_password.html', context)
