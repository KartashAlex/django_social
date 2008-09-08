from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('',
    (r'^$', 'django.views.generic.simple.redirect_to', {'url': '/accounts/register/'}),
    (r'^users/(\d+)/$', 'net.views.profile', {}, 'user_profile'),
    (r'^me/$', 'net.views.my_profile', {}, 'my_profile'),
    (r'^search/$', 'net.views.user_search', {}, 'user_search'),
    (r'^profile/$', 'net.views.edit_profile', {}, 'edit_user_profile'),
    (r'^profile/interests/$', 'net.views.edit_interests', {}, 'edit_user_interests'),
    (r'^profile/place/$', 'net.views.add_place', {}, 'add_user_place'),
    (r'^profile/place/(\d+)/$', 'net.views.edit_place', {}, 'edit_user_place'),
)

