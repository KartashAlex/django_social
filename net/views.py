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
from django.db.models import Q

from net.models import User, Friend, Place, TAG_FIELDS, NetGroup as Group
from net.forms import ProfileForm, InterestsForm, PlaceForm, FieldsetFormSet, GroupForm

def profile(request, id):
    from context_processors import widgets
    user = get_object_or_404(User, pk=id)
    
    return render_to_response('profile_t.html', {
        'profile': user,
        'widgets': widgets(request, user)['widgets'],
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
    query = Q()
    for key in TAG_FIELDS + ['interest', 'first_name', 'last_name', 'username', 'email', 'country__pk', 'city__pk', 'birthdate']:
        q = request.REQUEST.getlist(key) or request.REQUEST.getlist('q')
        if q:
            for subq in q:
                for subsubq in subq.split(' '):
                    query = query | Q(**{key+'__icontains': subsubq})

    users = User.objects.all()
    if query != Q():
        users = users.filter(query)
        
    return list_detail.object_list(request, queryset=users, template_name='users.html', paginate_by=10)

def friends(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    return list_detail.object_list(request, queryset=user.get_friends(), template_name='users.html', paginate_by=10)

@login_required
def change_friend(request, user_id, add):
    user = get_object_or_404(User, pk=user_id)
    if str(add) == "1":
        Friend.objects.get_or_create(friend=user, friend_of=request.user.user)
    else:
        try:
            Friend.objects.get(friend=user, friend_of=request.user.user).delete()
        except Friend.DoesNotExist:
            pass
    return HttpResponseRedirect(user.get_absolute_url())

def groups_list(request):
    return list_detail.object_list(request, queryset=Group.objects.all(), template_name='groups.html', paginate_by=10)

def groups_profile(request, group_id):
    return list_detail.object_detail(request, queryset=Group.objects.all(), object_id=group_id, template_name='group.html')
    
@login_required
def groups_create(request):
    if request.POST:
        form = GroupForm(data=request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.owner = request.user.user
            group.save()
            
            return HttpResponseRedirect('/me/')
    else:
        form = GroupForm()
    
    return render_to_response('group_create.html', {
        'form': form,
    }, context_instance=RequestContext(request))

@login_required
def groups_enter(request, group_id, enter):
    group = get_object_or_404(Group, pk=group_id)
    if str(enter) == "1":
        group.add_user(request.user.user)
    else:
        try:
            group.remove_user(request.user.user)
        except Group.UserException:
            pass
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/groups/'))
    
