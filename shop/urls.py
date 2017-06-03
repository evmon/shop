from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

from .views import ProductList, ProductDetail, Profile, add_comment, \
                    comment_approve, comment_remove, CommentList, Contact, \
                    Subscribe


app_name = 'shop'
# handler404 = 'show_404'

urlpatterns = [
    url(r'^$', Subscribe.as_view(template_name="shop/base.html"), name='home'),
    url(r'^login/$', auth_views.login, {'template_name': 'shop/account.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^profile/(?P<pk>[0-9]+)/$', Profile.as_view(), name='profile_form'),

    url(r'^comments/', CommentList.as_view(), name='comment-list'),
    url(r'^add-comment/$', add_comment, name='add-comment'),
    url(r'^comment/(?P<pk>\d+)/approve/$', comment_approve, name='comment_approve'),
    url(r'^comment/(?P<pk>\d+)/remove/$', comment_remove, name='comment_remove'),

    url(r'^contact/$', Contact.as_view(template_name="shop/contact.html"), name='contact'),
    # url(r'^detail/(?P<pk>[0-9]+)/$', ProductDetail.as_view(template_name="shop/detail.html"), name='detail'),
    

    url(r'^products/$', ProductList, name='ProductList'),
    url(r'^products/(?P<category_slug>[-\w]+)/$', ProductList, name='ProductListByCategory'),
    url(r'^products/(?P<id>\d+)/(?P<slug>[-\w]+)/$', ProductDetail, name='ProductDetail'),

    
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)