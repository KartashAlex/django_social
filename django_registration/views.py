"""
Views which allow users to create and activate accounts.

"""


from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from django_registration.forms import RegistrationForm, RegisterForm, TokenFormUniqueEmail, RegistrationFormUniqueEmail
from django_registration.models import RegistrationProfile, Token

from net.models import User as OurUser
from django.contrib.auth import login

def activate(request, activation_key, template_name='registration/activate.html'):
    activation_key = activation_key.lower() # Normalize before trying anything with it.
    account = RegistrationProfile.objects.activate_user(activation_key)
    return render_to_response(template_name,
                              { 'account': account,
                                'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS },
                              context_instance=RequestContext(request))

def activate_token(request, activation_key, template_name='registration/activate.html'):
    activation_key = activation_key.lower() # Normalize before trying anything with it.
    token = get_object_or_404(Token, activation_key=activation_key)
    if token.expired():
        return HttpResponseRedirect('/account/register/')
    try:
        user = token.get_user()
    except OurUser.DoesNotExist:
        user = token.create_user()
    login(request, user)
    return HttpResponseRedirect('/profile/')
    
def register(request, success_url='/accounts/register/complete/',
             form_class=RegistrationFormUniqueEmail, profile_callback=None,
             template_name='registration/registration_form.html'):
    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            new_user = form.save(profile_callback=profile_callback)
            return HttpResponseRedirect(success_url)
    else:
        form = form_class()
    return render_to_response(template_name,
                              { 'form': form },
                              context_instance=RequestContext(request))

def register_token(request, success_url='/accounts/register/complete/',
             form_class=TokenFormUniqueEmail, profile_callback=None,
             template_name='registration/registration_form.html'):
    if request.user.is_authenticated() and 'user' in dir(request.user):
        return HttpResponseRedirect('/me/')
    if request.POST:
        form = form_class(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect(success_url)
    else:
        form = form_class()
    request.session.set_test_cookie()
    return render_to_response(template_name,
                              { 'form': form },
                              context_instance=RequestContext(request))

