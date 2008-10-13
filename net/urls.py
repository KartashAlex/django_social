from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('',
    (r'^$', 'django.views.generic.simple.redirect_to', {'url': '/accounts/register/'}),
    (r'^users/(\d+)/$', 'net.views.profile', {}, 'user_profile'),
    (r'^me/$', 'net.views.my_profile', {}, 'my_profile'),
    (r'^search/$', 'net.views.user_search', {}, 'user_search'),
    (r'^users/$', 'net.views.user_search', {}, 'user_list'),
    (r'^profile/$', 'net.views.edit_profile', {}, 'edit_user_profile'),
    (r'^profile/interests/$', 'net.views.edit_interests', {}, 'edit_user_interests'),
    (r'^profile/place/$', 'net.views.add_place', {}, 'add_user_place'),
    (r'^profile/place/(\d+)/$', 'net.views.edit_place', {}, 'edit_user_place'),
    
    (r'^friends/(\d+)/$', 'net.views.friends', {}, 'list_friends'),
    (r'^friends/(\d+)/(\d)$', 'net.views.change_friend', {}, 'change_friend'),
    
    (r'^groups/$', 'net.views.groups_list', {}, 'groups_list'),
    (r'^groups/(\d+)/$', 'net.views.groups_profile', {}, 'groups_profile'),
    (r'^groups/(\d+)/enter/(\d)/$', 'net.views.groups_enter', {}, 'groups_enter'),
    (r'^groups/new/$', 'net.views.groups_create', {}, 'groups_create'),

    (r'^cities/(\d+)/$', 'net.views.ajax_cities', {}, 'ajax_cities'),
    (r'^places/template/$', 'net.views.ajax_places', {}, 'ajax_places'),
)

