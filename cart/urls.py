from django.conf.urls import url
from .views import CartDetail, CartRemove, CartAdd


urlpatterns = [
    url(r'^$', CartDetail, name='CartDetail'),
    url(r'^remove/(?P<product_id>\d+)/$', CartRemove, name='CartRemove'),
    url(r'^add/(?P<product_id>\d+)/$', CartAdd, name='CartAdd'),
]