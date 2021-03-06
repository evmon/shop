# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.shortcuts import  redirect, get_object_or_404
from django.views.decorators.http import require_POST


from shop.models import Product
from .cart import Cart
# from .forms import CartAddProductForm


# Create your views here.


# @require_POST
# def CartAdd(request, product_id):
#     cart = Cart(request)
#     product = get_object_or_404(Product, id=product_id)
#     form = CartAddProductForm(request.POST)
#     if form.is_valid():
#         cd = form.cleaned_data
#         cart.add(product=product, quantity=cd['quantity'],
#                                   update_quantity=cd['update'])
#     return redirect('cart:CartDetail')

@require_POST
def CartAdd(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product=product, )
    return redirect('cart:CartDetail')

def CartRemove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:CartDetail')

def CartDetail(request):
    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})