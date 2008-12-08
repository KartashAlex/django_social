# -*- coding:utf-8 -*-
from django.contrib.flatpages.models import FlatPage
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect

class LoginRedirectMiddleware:
    def process_request(self,request):
        if request.user.is_authenticated():
            return

        if request.path == '/accounts/login/' or \
           request.path == '/accounts/logout/' or \
           request.path.startswith('/accounts/activate/') or \
           request.path.startswith('/i/css/') or \
           request.path.startswith('/i/js/') or \
           request.path.startswith('/img/') or \
           request.path.startswith('/accounts/password/reset/') or \
           request.path.startswith('/accounts/reset/') or \
           request.path.startswith('/accounts/register/'):
            return

        if request.path in [fp.slug for fp in FlatPage.objects.all()]:
            return

        return HttpResponseRedirect('/accounts/login/')
