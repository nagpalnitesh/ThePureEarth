from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart
from django.urls import reverse
from .tasks import order_created


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        address = request.POST['address']
        city = request.POST['city']
        pincode = request.POST['pincode']

        order_obj = Order.objects.create(
            first_name=fname, last_name=lname, email=email, address=address, city=city, postal_code=pincode)
        order_obj.save()
        for item in cart:
            OrderItem.objects.create(order=order_obj,
                                     product=item['product'],
                                     price=item['price'],
                                     quantity=item['quantity'],)
            cart.clear()
            # set the order in the session
            request.session['order_id'] = order_obj.id
            # redirect for payment
            return redirect(reverse('payment:process'))
    else:
        form = OrderCreateForm()
        return render(request,
                      'orders/order/create.html',
                      {'cart': cart, 'form': form})


@ staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/admin/detail.html', {'order': order})
