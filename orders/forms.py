from django import forms
from .models import Order, OrderItem


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name','username', 'last_name', 'email', 'address', 'postal_code',
                  'city']

class UserOrder(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['id', 'paid']


class UserOrderDetail(forms.ModelForm):
    class Meta:
        model = OrderItem
        # fields = ['product', 'price', 'quantity']
        fields = ['product', 'price']