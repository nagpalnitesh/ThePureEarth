import razorpay
from django.shortcuts import render, get_object_or_404
from orders.models import Order, OrderItem
from cart.cart import Cart
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User
from pure.models import Profile

client = razorpay.Client(
    auth=('rzp_test_Ew6ZzFbU9SzCtp', 'Or5SJfy9sKMhThVFp1h0fN8Z'))

client.set_app_details({"title": "Django", "version": "1.8.17"})


def create_order(request):
    cart = Cart(request)
    currency = 'INR'
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    for item in cart:
        OrderItem.objects.create(order=order,
                                 product=item['product'],
                                 price=item['price'],
                                 quantity=item['quantity'])
        print(item['quantity'])
    print('order', order)
    amount = int(order.get_total_cost()*100)
    razorpay_amount = amount//100
    razorpay_order = client.order.create(dict(amount=amount,
                                              currency=currency,
                                              payment_capture='0'))

    razorpay_order_id = razorpay_order['id']
    callback_url = 'response/'

    context = {}
    context['order_id'] = order_id
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = 'rzp_test_Ew6ZzFbU9SzCtp'
    context['razorpay_amount'] = razorpay_amount
    context['currency'] = currency
    context['callback_url'] = callback_url

    return render(request, 'payment/created.html', context=context)


@csrf_exempt
def payment_process(request):
    cart = Cart(request)
    userauth_obj = Profile.objects.filter(user=request.user).first()
    print(userauth_obj.email)
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    # only accept POST request.
    if request.method == "POST":
        try:
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
            # verify the payment signature.
            result = client.utility.verify_payment_signature(
                params_dict)
            if result is not None:
                amount = int(order.get_total_cost())*100  # Rs. 200
                try:
                    # capture the payemt
                    client.payment.capture(payment_id, amount)
                    order.paid = True
                    order.braintree_id = payment_id
                    payment_fetch = client.payment.fetch(payment_id)
                    status = payment_fetch['status']
                    amount_fetch = payment_fetch['amount']
                    amount_fetch_inr = amount_fetch//100
                    order.save()
                    cart.clear()
                    if status == 'captured':
                        print('1')
                        try:
                            send_order_confirmation(userauth_obj, order_id)
                            send_order_confirmationUser(userauth_obj, order_id)
                        except:
                            return render(request, 'payment/done.html', {'amount': amount_fetch_inr, 'status': status})
                    # render success page on successful caputre of payment
                    return render(request, 'payment/done.html', {'amount': amount_fetch_inr, 'status': status})
                except:
                    cart.clear()
                    # if there is an error while capturing payment.
                    return render(request, 'payment/canceled.html')

            else:
                cart.clear()
                # if signature verification fails.
                return render(request, 'payment/canceled.html')
        except:
            print('79')
            cart.clear()
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
        cart.clear()
        print('82')
       # if other than POST request is made.
        return HttpResponseBadRequest()


def payment_done(request):
    cart = Cart(request)
    print('done', cart)
    cart.clear()
    return render(request, 'payment/done.html', {})


def payment_canceled(request):
    cart = Cart(request)
    print('canceled', cart)
    cart.clear()
    return render(request, 'payment/canceled.html', {})


def response(request):
    res = dict()
    res['order_id'] = request.GET.get('order_id')
    res['status'] = request.GET.get('status')
    res['signature'] = request.GET.get('signature')
    res['signature_algorithm'] = request.GET.get('signature_algorithm')
    print(res)
    return render(request, 'payment/done.html', {'res': res})


def send_order_confirmation(userauth_obj, orderId):
    email = userauth_obj.email
    name = userauth_obj.first_name.capitalize(
    ) + " " + userauth_obj.last_name.capitalize()
    subject = 'New Order Received on Your Website!'
    message = f'''Dear Ankur Khurana,

I hope this email finds you well. I am writing to inform you that a new order has been received on your website. Your customers are showing their trust and confidence in your products and services, and this is a testament to the hard work and dedication that you put into your business.

The order details are as follows:

Order Number: {orderId}
Customer Name: {name}
Email: {email}
It is important to promptly process this order and make sure that the customer receives their product in a timely manner. Please take the necessary actions to fulfill this order and keep your customer satisfied.

If you need any assistance, please do not hesitate to reach out to me. I am here to help in any way that I can.

Thank you for your time and attention.

Best regards,

The Pure Earth'''
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['jmsingh6871@gmail.com']
    try:
        send_mail(subject, message, email_from, recipient_list)
    except:
        print('mujhe neend aa rhi h, isliye m mail nhi bhej rha ')


def send_order_confirmationUser(userauth_obj, orderId):
    email = userauth_obj.email
    name = userauth_obj.first_name.capitalize(
    ) + " " + userauth_obj.last_name.capitalize()
    subject = 'Your Order Has Been Placed Successfully!'
    message = f'''Dear {name},
    
Thank you for shopping with us on our website! We are excited to inform you that your order has been placed successfully and we are working hard to fulfill it for you.

Your order details are as follows:

Order Number: {orderId}

We appreciate your business and are committed to providing you with excellent customer service. If you have any questions or concerns, please do not hesitate to reach out to us.

To track your order, please visit our website [Website URL]. This will give you the most up-to-date information on your order status and estimated delivery time.

Once again, thank you for shopping with us. We look forward to serving you again in the future.

Best regards,

The Pure Earth'''
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    try:
        send_mail(subject, message, email_from, recipient_list)
    except:
        print('mujhe neend aa rhi h, isliye m mail nhi bhej rha ')
