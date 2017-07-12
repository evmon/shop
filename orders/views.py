# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from decimal import Decimal

from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import OrderCreated

from liqpay.liqpay import LiqPay

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
                                         quantity=item['quantity'])
                # total = Order.objects.get_total_cost()
            

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