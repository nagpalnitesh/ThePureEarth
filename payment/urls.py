from django.urls import path, re_path, include
from . import views

app_name = 'payment'

urlpatterns = [
    path('process/', views.create_order, name="process"),
    path('response/', views.payment_process, name="payment_process"),
    path('canceled/', views.payment_canceled, name="canceled"),
    path('done/', views.payment_done, name="done"),
    # re_path(r'^paypal/', include('paypal.standard.ipn.urls'),name="paypal-ipn"),
]
