from django.conf.urls import url

from .views import OrderCreate, UserOrderList, UserOrderListDetail


app_name = 'order'
urlpatterns = [
    url(r'^create/$', OrderCreate, name='OrderCreate'),
    url(r'^history/$', UserOrderList.as_view(), name='orders-history'),
    url(r'^history/(?P<order_id>\d+)/detail/$', 
    	UserOrderListDetail, name='order-history-detail'),
]