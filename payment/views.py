import razorpay
from django.shortcuts import render, get_object_or_404
from orders.models import Order, OrderItem
from cart.cart import Cart
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest

client = razorpay.Client(
    auth=('rzp_test_Ew6ZzFbU9SzCtp', 'Or5SJfy9sKMhThVFp1h0fN8Z'))

client.set_app_details({"title": "Django", "version": "1.8.17"})


def create_order(request):
    cart = Cart(request)
    currency = 'INR'
    order_id = request.session.get('order_id')
    print(order_id)
    order = get_object_or_404(Order, id=order_id)
    for item in cart:
        OrderItem.objects.create(order=order,
                                 product=item['product'],
                                 price=item['price'],
                                 quantity=item['quantity'])
    print('order', order)
    amount = int(order.get_total_cost()*100)
    razorpay_amount = amount//100
    razorpay_order = client.order.create(dict(amount=amount,
                                              currency=currency,
                                              payment_capture='0'))

    razorpay_order_id = razorpay_order['id']
    callback_url = 'response/'

    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = 'rzp_test_Ew6ZzFbU9SzCtp'
    context['razorpay_amount'] = razorpay_amount
    context['currency'] = currency
    context['callback_url'] = callback_url

    return render(request, 'payment/created.html', context=context)


@csrf_exempt
def payment_process(request):
    cart = Cart(request)
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
                    # render success page on successful caputre of payment
                    return render(request, 'payment/done.html', {'amount': amount_fetch_inr, 'status': status})
                except:
                    # if there is an error while capturing payment.
                    return render(request, 'payment/canceled.html')

            else:
                # if signature verification fails.
                return render(request, 'payment/canceled.html')
        except:
            print('79')
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
        print('82')
       # if other than POST request is made.
        return HttpResponseBadRequest()
    # order_id = request.session.get('order_id')
    # order = get_object_or_404(Order, id=order_id)
    # print("Payment", order)
    # if request.method == "POST":
    #     order.paid = True
    #     print("Payment order", order.paid)
    #     orderitem = get_object_or_404(OrderItem, order=order)
    #     print("Order Item", orderitem.get_cost())
    #     amount = int(orderitem.get_cost())*100
    #     amount_inr = amount//100
    #     print("Amount ", amount)
    #     print("Type amount str to int ", amount)
    #     payment_id = request.POST['razorpay_payment_id']
    #     order.braintree_id = payment_id
    #     order.save()
    #     # print("Multiple value",payment_id)
    #     print("Payment Id", payment_id)
    #     payment_client_capture = (client.payment.capture(payment_id, amount))
    #     print("Payment Client capture", payment_client_capture)
    #     payment_fetch = client.payment.fetch(payment_id)
    #     status = payment_fetch['status']
    #     amount_fetch = payment_fetch['amount']
    #     amount_fetch_inr = amount_fetch//100
    #     print("Payment Fetch", payment_fetch['status'])
    #     return render(request, 'payment/done.html', {'amount': amount_fetch_inr, 'status': status})


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
