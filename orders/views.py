# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.views.generic import ListView, DetailView
from decimal import Decimal

from .models import OrderItem, Order
from .forms import OrderCreateForm, UserOrder, UserOrderDetail
# from .forms import UserOrder, UserOrderDetail
from cart.cart import Cart
from .tasks import OrderCreated

# from liqpay.liqpay import LiqPay

def OrderCreate(request):
    cart = Cart(request)
    total = cart.get_total_price()
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'],
                                         price=item['price'],
                                         # quantity=item['quantity']
                                         )
            cart.clear()
            OrderCreated(order.id)

            liqpay = LiqPay('i51254763270', 'n2GrFM1QkVB9zTlQdtFu8NzneL56TfMzmFGJQaeC')
            html = liqpay.cnb_form({
               
                    "action": "pay",
                    "amount": str(total),
                    "currency": "USD",
                    "description": "Order id: " + str(order.id),
                    "order_id": str(order.id),
                    "version": "3",
                    "language": "en",
                    # "sandbox": "1",
                })
            
            
            return render(request, 'orders/created.html', {'order': order, 'html': html})

    form = OrderCreateForm()
    
    return render(request, 'orders/create.html', {'cart': cart, 'form': form})


class UserOrderList(ListView):
    models = Order
    form_class = UserOrder
    template_name = 'orders/detail.html'
    context_object_name = 'order_history'
    queryset = Order.objects.all()


def UserOrderListDetail(request, order_id):
    order = OrderItem.objects.filter(order=order_id)
    return render(request, 'orders/order_detail.html', {'order_history_detail': order})