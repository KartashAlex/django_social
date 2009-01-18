# -*- coding: UTF-8 -*-

"""
URLConf for Django user registration.

Recommended usage a call to ``include()`` in your project's root
URLConf to include this URLConf for any URL beginning with
``/accounts/``.

"""
from django.conf import settings

from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
import django.contrib.auth.views

from django_registration.views import activate_token, register_token

urlpatterns = patterns('',
                       # Activation keys get matched by \w+ instead of the more specific
                       # [a-fA-F0-9]{40} because a bad activation key should still get to the view;
                       # that way it can return a sensible "invalid key" message instead of a
                       # confusing 404.
                       url(r'^activate/(?P<activation_key>\w+)/$',
                           activate_token,
                           name='registration_activate'),
                       url(r'^login/$',
                           'django.contrib.auth.views.login',
                           {'template_name': 'registration/login.html'},
                           name='auth_login'),
                       url(r'^logout/$',
                           'django.contrib.auth.views.logout',
                           {'template_name': 'registration/logout.html', 'next_page': settings.LOGOUT_REDIRECT_URL},
                           name='auth_logout'),
                       url(r'^password/change/$',
                           'django.contrib.auth.views.password_change',
                           name='auth_password_change'),
                       url(r'^password/change/done/$',
                           'django.contrib.auth.views.password_change_done',
                           name='auth_password_change_done'),
                           
                       url(r'^password/reset/$',
                           'django.contrib.auth.views.password_reset',
                           name='auth_password_reset'),
                           
                       url(r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 
                           'django.contrib.auth.views.password_reset_confirm', 
                           name='password_reset_confirm'),
                        
                       url(r'^password/reset/done/$',
                           'django.contrib.auth.views.password_reset_done',
                           {'template_name': 'registration/reset_done.html'},
                           name='auth_password_reset_done'),

                       url(r'^password/reset/complete/$',
                           'django.contrib.auth.views.password_reset_complete',
                           {'template_name': 'registration/password_reset_complete.html'},
                           name='auth_password_reset_complete'),

                       url(r'^register/$',
                           register_token,
                           name='registration_register'),
                       url(r'^register/complete/$',
                           direct_to_template,
                           {'template': 'registration/registration_complete.html'},
                           name='registration_complete'),
                       )
