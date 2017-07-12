# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.urlresolvers import reverse
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import User, AbstractBaseUser, PermissionsMixin

from django.utils import timezone

class CommonProductInfo(models.Model):

    img = models.ImageField()
    title = models.CharField(max_length=200, verbose_name='Title')
    description = models.CharField(max_length=1000, verbose_name='Description')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Price')
    manufacturer = models.CharField(max_length=50, verbose_name='Manufacturer')
    color = models.CharField(max_length=50, verbose_name='Color')
    stock = models.PositiveIntegerField(verbose_name="Stock")
    available = models.BooleanField(default=True, verbose_name="Available")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=200, db_index=True)

    class Meta:
        abstract = True

@python_2_unicode_compatible
class Category(models.Model): 

	name = models.CharField(max_length=128) 
	slug = models.SlugField(max_length=200, db_index=True, unique=True)

	class Meta: 
		ordering = ['name']
		verbose_name = 'Category' 
		verbose_name_plural = 'Categories' 

	def get_absolute_url(self):
		return reverse('shop:ProductListByCategory', args=[self.slug])

	def __str__(self): 
		return '{0}'.format(self.name)


@python_2_unicode_compatible
class Product(CommonProductInfo):

	category = models.ForeignKey('Category')

	class Meta:

		ordering = ['title']
		index_together = [['id', 'slug']]
		verbose_name = 'Product' 
		verbose_name_plural = 'Products' 

	def get_absolute_url(self):
		return reverse('shop:ProductDetail', args=[self.id, self.slug])

	def __str__(self):
		return '{0}'.format(self.title)
 	

@python_2_unicode_compatible
class Comment(models.Model):

    post = models.ForeignKey('Product', related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return '{0} | {1}'.format(self.author, self.text, self.approved_comment )


@python_2_unicode_compatible
class ContactUserForm(models.Model):

    name = models.CharField(max_length=128) 
    email = models.EmailField(
        help_text=('email address'),
        blank=False,
    )
    msg = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    check_msg = models.BooleanField(default=False)

    def approve(self):
        self.check_msg = True
        self.save()

    def __str__(self):
        return '{0} | {1}: {2}'.format(self.created_date, self.email, self.msg )


@python_2_unicode_compatible
class Subscribe(models.Model):

    email = models.EmailField(
        help_text=('email address'),
        blank=False,
        unique = True,
    )
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '{0} | {1}'.format(self.created_date, self.email)