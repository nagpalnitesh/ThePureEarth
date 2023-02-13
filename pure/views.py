import uuid
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from orders.models import Order, OrderItem
from .models import *
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# from django.views.decorators.http import require_POST
from .helpers import send_forget_password_token, send_username
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from cart.forms import *

# Create your views here.


# Home page
def home(request):
    return render(request, 'screens/Home.html')


# Error Page
def handler404(request, exception):
    return redirect(request, 'screens/error.html', {}, status=404)


def handler500(request, *args, **argv):
    return render(request, 'screens/error.html', status=500)


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
    userauth_obj = Profile.objects.filter(user=request.user).first()
    getUser = User.objects.get(id=userauth_obj.user.id)
    orders = Order.objects.filter(user=userauth_obj).order_by('-id')
    if request.method == 'POST':
        update_firstName = request.POST['upfname']
        update_lastName = request.POST['uplname']
        update_phoneNumber = request.POST['upnumber']
        update_email = request.POST['upemail']
        update_password = request.POST['pass2']
        update_confPassword = request.POST['confpass1']
        try:
            if User.objects.filter(email=update_email).exclude(id=userauth_obj.user.id):
                messages.error(request, 'Email already exists')
                return redirect('/profile')
            if update_password != update_confPassword:
                messages.error(
                    request, 'Password and Confirm Password does not match')
                return redirect('/profile')
            if len(update_password) < 8:
                messages.error(
                    request, 'Password must be atleast 8 characters')
                return redirect('/profile')
            if len(update_phoneNumber) < 10 or len(update_phoneNumber) > 10:
                messages.error(
                    request, 'Phone number is not valid')
                return redirect('/profile')
            getUser.set_password(update_password)
            getUser.save()
            User.objects.filter(id=userauth_obj.user.id).update(
                email=update_email, first_name=update_firstName, last_name=update_lastName)
            Profile.objects.filter(user=request.user).update(
                email=update_email, first_name=update_firstName, last_name=update_lastName, phone_number=update_phoneNumber)
            messages.success(
                request, 'Your The Pure Earth account has been successfully updated')
            logout(request)
            return redirect('/login')
        except Exception as e:
            print('Error', e)
            messages.error(request, 'Something went wrong')
            return redirect('/profile')
    return render(request, 'dashboard/profile.html', {'orders': orders, 'profile': userauth_obj})


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
        user_auth_obj = Profile.objects.filter(user=user).first()

        if user is None:
            messages.error(request, 'Invalid Credentials! Please Try Again')
            return redirect('/login')

        else:
            user_auth_obj = Profile.objects.filter(user=user).first()

            print(user_auth_obj, user)

            if not user_auth_obj.is_Verified:
                messages.error(request, 'Please verify your account')
                return redirect('/login')

            if user is not None:
                login(request, user)
                messages.success(
                    request, 'You have been logged in successfully')
                return redirect('/')

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
        firstname = request.POST['fname']
        lastname = request.POST['lname']
        phone_number = request.POST['phone_number']
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
                messages.error(
                    request, 'Password and Confirm Password does not match')
                return redirect('/signup')
            if len(pass1) < 8:
                messages.error(
                    request, 'Password must be atleast 8 characters')
            if len(phone_number) < 10 or len(phone_number) > 10:
                messages.error(
                    request, 'Phone number is not valid')
                return redirect('/signup')
            if len(username) < 6 and not username.isalnum():
                messages.error(
                    request, 'Username must be atleast 8 characters')
                messages.error(
                    request, 'Username should contain only letters and numbers')
                return redirect('/signup')
            auth_token = str(uuid.uuid4())
            user_obj = User.objects.create(
                username=username, email=email, first_name=firstname, last_name=lastname)
            user_obj.set_password(pass1)
            user_obj.save()
            user_profile = Profile.objects.create(
                user=user_obj, phone_number=phone_number, email=email, first_name=firstname, last_name=lastname, auth_token=auth_token)
            user_profile.save()
            messages.success(
                request, 'Your The Pure Earth account has been successfully created')
            messages.success(
                request, 'Please check your email for verification')
            activate_account(email, auth_token)
            return redirect('/login')
        except Exception as e:
            print('Error', e)
            messages.error(request, 'Something went wrong')
            return redirect('/signup')

    return render(request, 'registration/signup.html')


# activate account function
def activate_account(email, token):
    subject = 'Activate your account'
    message = f'''Hi,

We hope this email finds you well. We're writing to let you know that you recently signed up for an account on Pure Earth, the online platform that connects individuals and organizations with sustainability initiatives around the world.

To complete your profile and start making a positive impact, we need to verify your email address. This is a quick and easy step that helps us ensure that you are who you say you are.

Please click on the link below to verify your Pure Earth profile:

https://thepureearth.com/verify/{token}

If you did not sign up for an account on Pure Earth, please ignore this email and your account will not be created.

We're excited to have you on board and can't wait to see the positive impact you will make in the world!

Best regards,

The Pure Earth Team'''
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)


# verification function
def verify(request, auth_token):
    try:
        user_auth_obj = Profile.objects.filter(auth_token=auth_token).first()
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
@csrf_exempt
def forget_password(request):
    try:
        if request.method == 'POST':
            email = request.POST.get('femail')
            user_obj = User.objects.filter(email=email).first()
        if user_obj is None:
            messages.error(request, 'No user found')
            return redirect('/forgot-password')
        user_obj = User.objects.get(email=email)
        token = str(uuid.uuid4())
        send_forget_password_token(user_obj.email, token)
        userauth_obj = Profile.objects.get(user=user_obj)
        userauth_obj.forget_password_token = token
        userauth_obj.save()
        messages.success(request, 'Reset Password Sent')
        messages.success(
            request, 'Please check your email for reset password link')
        return redirect('/login')
    except Exception as e:
        print(e)
    return render(request, 'registration/forget.html')


# change password
def change_password(request, token):
    context = {}
    try:
        user_auth_obj = Profile.objects.filter(
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
            print(newpass, newconfpass)
            user_obj = User.objects.get(id=user_id)
            user_obj.set_password(newpass)
            user_obj.save()
            print(user_obj)
            messages.success(request, 'Password changed successfully')
            return redirect('/login')

    except Exception as e:
        print(e)

    return render(request, 'registration/change_password.html', context)


# froger username
@csrf_exempt
def forgot_username(request):
    try:
        if request.method == 'POST':
            email = request.POST.get('femail')
            user_obj = User.objects.filter(email=email).first()
        if user_obj is None:
            messages.error(request, 'No user found')
            return redirect('/forget-username')
        user_obj = User.objects.get(
            email=email)
        send_username(user_obj.email, user_obj.username)
        messages.success(
            request, 'Please check your email for username')
        return redirect('/login')
    except Exception as e:
        print(e)

    return render(request, 'registration/forget_username.html')

# Product List and Details Page
# Product List


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(is_active=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'screens/Products.html', {'category': category, 'categories': categories, 'products': products})

# Product Details


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    cart_product_form = CartAddProductForm()
    return render(request,
                  'screens/ProductDetail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form})


# Order Detail
# def orderdetail(request, id):
#     order = Order.objects.get(pk=id)
#     orderitems = OrderItem.objects.filter(order=order).order_by('-id')
#     return render(request, 'dashboard/orders.html', {'orderitems': orderitems})
