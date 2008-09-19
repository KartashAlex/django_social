# -*- coding: UTF-8 -*-

from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.conf import settings
from django.views.generic import list_detail
from django.core import serializers
from django.forms.formsets import formset_factory
from django.contrib.auth.decorators import login_required

from net.models import User, Place, TAG_FIELDS
from net.forms import ProfileForm, InterestsForm, PlaceForm, FieldsetFormSet

def profile(request, id):
    from context_processors import widgets
    user = get_object_or_404(User, pk=id)
    
    return render_to_response('profile_t.html', {
        'profile': user,
        'widgets': widgets(request, user),
    }, context_instance=RequestContext(request))

@login_required
def my_profile(request):
    try:        
        user = request.user.user
    except User.DoesNotExist:
        return HttpResponseRedirect('/')
    
    return render_to_response('profile_t.html', {
        'profile': user,
    }, context_instance=RequestContext(request))
    
def get_dict(qs):
    result = []
    for item in qs:
        item_dict = {}
        for f in item._meta.fields:
            try:
                item_dict[f.name] = item.__getattribute__(f.name).pk
            except AttributeError:
                item_dict[f.name] = item.__getattribute__(f.name)
        result += [item_dict]
    return result
    
@login_required
def edit_profile(request):
    if request.POST:
        form = ProfileForm(data=request.POST, files=request.FILES, instance=request.user.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/me/')
    else:
        form = ProfileForm(instance=request.user.user)
     
        
    return render_to_response('edit_profile.html', {
        'form': form,
        'profile': request.user.user,
    }, context_instance=RequestContext(request))
    
@login_required
def add_place(request):
    if request.POST:
        form = PlaceForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save(user=request.user.user)
            return HttpResponseRedirect('/me/')
    else:
        form = PlaceForm(instance=request.user.user)
     
        
    return render_to_response('edit_place.html', {
        'form': form,
        'profile': request.user.user,
    }, context_instance=RequestContext(request))
    
@login_required
def edit_place(request, id):
    place = get_object_or_404(Place, pk=id, user=request.user.user)
    if request.POST:
        form = PlaceForm(data=request.POST, files=request.FILES, instance=place)
        if form.is_valid():
            form.save(user=request.user.user)
            return HttpResponseRedirect('/me/')
    else:
        form = PlaceForm(instance=place)
     
        
    return render_to_response('edit_place.html', {
        'form': form,
        'profile': request.user.user,
    }, context_instance=RequestContext(request))

@login_required
def edit_interests(request):
    if request.POST:
        form = InterestsForm(data=request.POST, files=request.FILES, instance=request.user.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/me/')
    else:
        form = InterestsForm(instance=request.user.user)
        
    return render_to_response('edit_profile.html', {
        'form': form,
        'profile': request.user.user,
    }, context_instance=RequestContext(request))

def user_search(request):
    kwargs = {}
    print request.GET
    for key in TAG_FIELDS + ['interest', 'schools__title']:
        if request.GET.get(key):
            kwargs[key+'__icontains'] = request.GET.get(key)

    print kwargs

    users = User.objects.filter(**kwargs)
    return list_detail.object_list(request, queryset=users, template_name='users.html')
