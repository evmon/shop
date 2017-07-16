# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import FormView, UpdateView, ListView, \
                                DetailView, CreateView
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.shortcuts import get_object_or_404, HttpResponse
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import ModelFormMixin
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect

from registration.forms import RegistrationFormUniqueEmail

from cart.forms import CartAddProductForm
from .forms import UserForm, CommentForm, ContactForm, \
                    SubscribeForm
from .models import Product, Category, Comment, ContactUserForm, Subscribe



def ProductList(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'shop/product_list.html', {
        'category': category,
        'categories': categories,
        'products': products
    })


class ProductDetail(DetailView):

    model = Product
    context_object_name = 'product'
    template_name = 'shop/detail.html'
    def get_context_data(self, **kwargs):
        context = super(ProductDetail, self).get_context_data(**kwargs)
        context['cart_product_form'] = CartAddProductForm()        
        return context



class CommentList(ListView):
    model = Comment
    template_name = "shop/comment_list.html"
    queryset = Comment.objects.all()
        
        

class Profile(UpdateView):
    """
    Class to display user profile in detail

    """
    model = User
    form_class = UserForm
    template_name = "shop/profile_form.html"
    success_url= '/'

    


class Contact(CreateView):
    """
    Class to display user profile in detail

    """
    model = ContactUserForm
    form_class = ContactForm
    success_url= '/'


class Subscribe(CreateView):
    """
    Class to display user profile in detail

    """
    model = Subscribe
    form_class = SubscribeForm
    success_url= '/'
    template_name='shop/base.html'


class Search(ListView):

    model = Product
    template_name = 'shop/search_list.html'
    
    def get_queryset(self):
        queryset = Product.objects.all()
        var_get_search = self.request.GET.get('search_box')

        if var_get_search is not None:
            queryset = queryset.filter(title__icontains=var_get_search)
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super(Search, self).get_context_data(**kwargs)
        context['count'] = self.get_queryset().count()
        return context

  
@login_required
def comment_approve(request, pk, slug):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    post_slug = comment.post.slug
    comment.approve()
    return redirect('shop:ProductDetail', pk=post_pk, slug=post_slug)

@login_required
def comment_remove(request, pk, slug):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    post_slug = comment.post.slug
    comment.delete()
    return redirect('shop:ProductDetail', pk=post_pk, slug=post_slug)

def add_comment(request, pk, slug):
    post = get_object_or_404(Product, pk=pk, slug=slug)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()

            return redirect('shop:ProductDetail', pk=post.pk, slug=post.slug)
    else:
        form = CommentForm()
    return render(request, 'shop/add_comment.html', {'form': form})

