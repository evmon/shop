# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.contrib.auth.models import User

from .models import Comment, ContactUserForm, Subscribe



class UserForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'email']



class CommentForm(forms.ModelForm):
	
	class Meta():

		model = Comment
		fields = ['author','text',]
		widgets = {
			'author': forms.TextInput( attrs={'class':'form-control', 'label':'Your name',}),
			'text': forms.TextInput( attrs={'class':'form-control', 'label':'Your message',}),
			}

class ContactForm(forms.ModelForm):
	class Meta():
		model = ContactUserForm
		fields = ['name', 'email', 'msg']
		widgets = {
			'msg': forms.TextInput( attrs={'resize': 'none',}),
			}


class SubscribeForm(forms.ModelForm):
	
	class Meta():

		model = Subscribe
		fields = ['email']
		widgets = {
			'email': forms.TextInput( attrs={
				'placeholder': 'Enter your email here...',
				'style':' margin-right:10px; ',
				})
			}