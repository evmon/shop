# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import FormView, UpdateView, ListView, DetailView, CreateView
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.shortcuts import get_object_or_404, HttpResponse
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import ModelFormMixin

from cart.forms import CartAddProductForm
from .forms import UserForm, CommentForm, ContactForm, SubscribeForm
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


def ProductDetail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()


    return render(request, 'shop/detail.html',
                             {'product': product,
                              'cart_product_form': cart_product_form})


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

    


    def form_valid(self, form):
        
        self.object = form.save()
        return super(ModelFormMixin, self).form_valid(form)

    def form_invalid(self, form):
        
        return self.render_to_response(self.get_context_data(form=form))


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('shop:comment-list', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('shop:comment-list', pk=post_pk)


def add_comment(request, pk):
    post = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('shop:comment-list', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'shop/add_comment.html', {'form': form})