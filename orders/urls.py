from django.conf.urls import url
from .views import OrderCreate


urlpatterns = [
    url(r'^create/$', OrderCreate, name='OrderCreate')
]