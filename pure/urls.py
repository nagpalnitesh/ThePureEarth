"""Pure App URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from . import views


app_name = 'pure'

urlpatterns = [
    path('', views.home, name='home'),  # home page
    path('aboutus', views.about, name='about'),  # about page
    path('contact', views.contact, name='contact'),  # contact page
    path('faq', views.faq, name='faq'),  # faq page
    path('terms-and-conditions', views.tnc, name='terms'),  # terms page
    path('privacy-policy', views.privacy, name='privacy'),  # privacy page
    path('return-policy', views.Return, name='returns'),  # returns page
    path('shipping-policy', views.shipping, name='shipping'),  # shipping page

    # user auth urls
    path('login', views.handleLogin, name='login'),  # login page
    path('logout', views.handleLogout, name='logout'),  # logout page
    path('signup', views.handleSignup, name='register'),  # register page
    #verify account
    path('verify/<auth_token>', views.verify, name='verify'),
    path('error', views.error, name='error'),  # error page
    path('forgot-password', views.forget_password, name='forgot'),  # forgot password page
    path('reset-password/<token>', views.change_password, name='reset'),  # reset password page

    # products urls
    path('products', views.product_list, name='products_list'),  # products page
    path('product/<slug:slug>', views.product_detail, name='product_detail'),  # product detail page
    path('cart',views.cart_detail,name='cart_detail'),
    path('add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
]
