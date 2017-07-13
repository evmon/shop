# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from celery import task
from django.core.mail import send_mail
from .models import Order


@task
def OrderCreated(order_id):
    
    order = Order.objects.get(id=order_id)
    subject = 'Order number {}'.format(order.id)
    message = 'Dear, {} {}, you are successfully placed an order.\
               Order number {}'.format(order.first_name, order.last_name, order.id)
    mail_send = send_mail(subject, message, 'zheny.mon@gmail.com', [order.email])
    return mail_send