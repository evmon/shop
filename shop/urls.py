from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

from registration.forms import RegistrationFormUniqueEmail
from registration.backends.simple.views import RegistrationView
from .views import ProductList, ProductDetail, Profile, add_comment, \
                    comment_approve, comment_remove, CommentList, Contact, \
                    Subscribe, Search

 
app_name = 'shop'
# handler404 = 'show_404'

urlpatterns = [
    url(r'^$', Subscribe.as_view(), name='home'),
    url(r'^login/$', auth_views.login, {
        'template_name': 'registration/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^register/$', RegistrationView.as_view(
        success_url='registration_complete'
        ), name='registration_register'),
    url(r'^register-complete/$', TemplateView.as_view(
        template_name="registration/registration_complete.html"
        ), name='registration_complete'),
    url(r'^user/password/reset/$', auth_views.password_reset,{
        'template_name': 'registration_shop/password_reset_form.html', 
        'post_reset_redirect' : '/user/password/reset/done/'},
        name="password_reset"),
    url(r'^user/password/reset/done/$', auth_views.password_reset_done, {
        'template_name': 'registration_shop/password_reset_done.html'},
        name="password_reset_done"),
    url(r'^user/password/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', 
        auth_views.password_reset_confirm, {
        'template_name': 'registration_shop/password_reset_confirm.html',
        'post_reset_redirect' : '/user/password/done/' },
        name="password_reset_confirm"),
    url(r'^user/password/done/$', auth_views.password_reset_complete,
        {'template_name': 'registration_shop/password_reset_complete.html'}, 
        name="password_reset_complete"),
    url(r'^search/$', Search.as_view(), name='search'),
    url(r'^profile/(?P<pk>[0-9]+)/$', Profile.as_view(), name='profile_form'),
    url(r'^contact/$', Contact.as_view(
        template_name="shop/contact.html"), name='contact'),
    url(r'^products/$', ProductList, name='ProductList'),
    url(r'^products/(?P<category_slug>[-\w]+)/$', ProductList, name='ProductListByCategory'),
    url(r'^products/(?P<pk>\d+)/(?P<slug>[-\w]+)/$', ProductDetail.as_view(), name='ProductDetail'),
    url(r'^product/(?P<pk>\d+)/(?P<slug>[-\w]+)/add-comment/$', add_comment, name='add-comment'),
    url(r'^comment/(?P<pk>\d+)/(?P<slug>[-\w]+)/approve/$', comment_approve, name='comment_approve'),
    url(r'^comment/(?P<pk>\d+)/(?P<slug>[-\w]+)/remove/$', comment_remove, name='comment_remove'),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)