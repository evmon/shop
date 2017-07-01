# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Product, Category, Comment, ContactUserForm, Subscribe


class CategoryAdmin(admin.ModelAdmin):
	"""
	Category model
	list_display: fields listed in list_editable will be displayed as form widgets on the change list page
	prepopulated_fields: the generated value is produced by concatenating the values of the source fields

	"""
	list_display = ['name', 'slug']
	prepopulated_fields = {'slug': ('name', )}


class ProductAdmin(admin.ModelAdmin):
	"""
	Product model
	list_filter: activate filters in the right sidebar of the change list page of the admin

	"""

	list_display = ['title', 'slug', 'price', 'stock', 'available', 'created', 'updated']
	list_filter = ['available', 'created', 'updated']
	list_editable = ['price', 'stock', 'available']
	prepopulated_fields = {'slug': ('title', )}

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Comment)
admin.site.register(ContactUserForm)
admin.site.register(Subscribe)
