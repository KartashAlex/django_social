# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('django_authopenid.views',
     # manage account registration
    url(r'^signin/$', 'signin', name='user_signin'),
    url(r'^signout/$', 'signout', name='user_signout'),
    url(r'^signin/complete/$', 'complete_signin', name='user_complete_signin'),
    url(r'^register/$', 'register', name='user_register'),
    url(r'^signup/$', 'signup', name='user_signup'),
    url(r'^sendpw/$', 'sendpw', name='user_sendpw'),
    url(r'^password/confirm/$', 'confirmchangepw', name='user_confirmchangepw'),

    # manage account settings
    url(r'^$', 'account_settings', name='user_account_settings'),
    url(r'^password/$', 'changepw', name='user_changepw'),
    url(r'^email/$', 'changeemail', name='user_changeemail'),
    url(r'^openid/$', 'changeopenid', name='user_changeopenid'),
    url(r'^delete/$', 'delete', name='user_delete'),
)
