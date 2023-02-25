from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404

from pure.models import Profile
from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart
from django.urls import reverse
from django.contrib import messages


def order_create(request):
    cart = Cart(request)
    orderId = request.session.get('order', [])
    print('orderId', orderId)
    current_user = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        phone = request.POST['phone']
        address = request.POST['address']
        city = request.POST['city']
        pincode = request.POST['pincode']

        if len(phone) < 10 or len(phone) > 10:
            messages.error(
                request, 'Phone number is not valid')
            return redirect('/orders/create')

        order_obj = Order.objects.create(user=current_user,
                                         first_name=fname, last_name=lname, phone=phone, address=address, city=city, postal_code=pincode)
        request.session['order_id'] = order_obj.id
        order_obj.save()
        # set the order in the session
        # request.session['order_id'] = order_obj.id
        # redirect for payment
        return redirect(reverse('payment:process'))
        # return render(request, 'payment:process')
    else:
        form = OrderCreateForm()
        return render(request,
                      'orders/order/create.html',
                      {'cart': cart, 'form': form})


@ staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    return render(request, 'orders/admin/detail.html', {'order': order})


def my_order_details(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/admin/detail.html', {'order': order})
