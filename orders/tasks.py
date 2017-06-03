# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from celery import task
from django.core.mail import send_mail
from .models import Order


@task
def OrderCreated(order_id):
    
    order = Order.objects.get(id=order_id)
    subject = 'Заказ c номером {}'.format(order.id)
    message = 'Дорогой, {}, вы успешно сделали заказ.\
               Номер вашего заказа {}'.format(order.first_name, order.id)
    mail_send = send_mail(subject, message, 'admin@shop.com', [order.email])
    return mail_send