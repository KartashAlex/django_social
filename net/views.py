# -*- coding: UTF-8 -*-

from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django.template import RequestContext
from django.conf import settings
from django.views.generic import list_detail
from django.core import serializers
from django.forms.formsets import formset_factory
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from net.models import User, Friend, Place, PlaceTemplate, TAG_FIELDS, NetGroup as Group, City, Event
from net.forms import ProfileForm, InterestsForm, PlaceForm, FieldsetFormSet, GroupForm, SearchForm

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
        form = PlaceForm()
     
    if request.GET.get('ajax'):
        tpl = 'edit_place_ajax.html'
    else:
        tpl = 'edit_place.html'
        
    return render_to_response(tpl, {
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
     
    if request.GET.get('ajax'):
        tpl = 'edit_place_ajax.html'
    else:
        tpl = 'edit_place.html'
        
    return render_to_response(tpl, {
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

@login_required
def user_search(request):
    query = Q()
    I18N_FIELDS = [
        'country__pk', 'city__pk',
        'places__template__translations__name', 'places__template__city__country__translations__name',
        'places__template__city__translations__name',
    ]
    TEXT_SEARCH = TAG_FIELDS + I18N_FIELDS + ['interest', 'first_name', 'last_name', 'username', 'email']
    OTHER_SEARCH = ['birthdate']
    for key in TEXT_SEARCH + OTHER_SEARCH:
        q = request.REQUEST.getlist(key) or request.REQUEST.getlist('q')
        if q and q != '' and q != [] and q != ['']:
            for subq in q:
                for subsubq in subq.split(' '):
                    if key in TEXT_SEARCH:
                        query = query | Q(**{key+'__icontains': subsubq})
                    else:
                        if request.REQUEST.getlist(key):
                            query = query | Q(**{key: subsubq})

    users = User.objects.all()
    if query and query.children:
        users = users.filter(query)
    users = users.distinct()
    
    if request.POST:
        form = SearchForm(request.POST)
        qdict = form.get_query()
        if qdict:
            users = users.filter(**qdict)
    else:
        form = SearchForm()
        
    return list_detail.object_list(request, 
        queryset=users, template_name='users.html', 
        paginate_by=10, extra_context={'form': form}
    )

@login_required
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

@login_required
def groups_list(request, my=False):
    groups = Group.objects.all()
    if my:
        try:
            groups = groups.filter(members=request.user.user)
        except:
            pass

    query = Q()
    TEXT_SEARCH = ['name', 'description', 'posts__subject', 'posts__text', 'albums__photos__title', 'albums__title', 'interest']
    OTHER_SEARCH = []
    for key in TEXT_SEARCH + OTHER_SEARCH:
        q = request.REQUEST.getlist(key) or request.REQUEST.getlist('q')
        if q and q != '' and q != [] and q != ['']:
            for subq in q:
                for subsubq in subq.split(' '):
                    if key in TEXT_SEARCH:
                        query = query | Q(**{key+'__icontains': subsubq})
                    else:
                        if request.REQUEST.getlist(key):
                            query = query | Q(**{key: subsubq})
    if query and query.children:
        groups = groups.filter(query)

    return list_detail.object_list(request, queryset=groups, template_name='groups.html', paginate_by=10)

@login_required
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
            
            return HttpResponseRedirect(group.get_absolute_url())
    else:
        form = GroupForm()
    
    return render_to_response('group_create.html', {
        'form': form,
    }, context_instance=RequestContext(request))

@login_required
def groups_enter(request, group_id, enter):
    group = get_object_or_404(Group, pk=group_id)
    url = request.META.get('HTTP_REFERER', '/groups/')
    if str(enter) == "1":
        group.add_user(request.user.user)
    else:
        try:
            group.remove_user(request.user.user)
        except Group.UserException:
            url = url + '?error=your_group'
    return HttpResponseRedirect(url)
    
@login_required
def groups_invite(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    user = get_object_or_404(User, pk=request.REQUEST.get('user'))
    Event.objects.create_event(request.user.user, user=user, type='group_invite', group=group)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/groups/'))
    
def json(lst, fields):
    s1 = []
    for l in lst:
        s = u'{'
        s0 = []
        for k in fields:
            s0.append(u'"%s": "%s"' % (k, l.__getattribute__(k)))
        s += u'%s}' % u','.join(s0)
        s1.append(s)
    return u'[%s]' % ',\n'.join(s1)
    
def ajax_cities(request, country_id):
    cities = City.objects.filter(country__pk=country_id)
    return HttpResponse(json(cities, ['id', 'name']), mimetype="text/javascript")

def ajax_places(request):
    places = PlaceTemplate.objects.all()
    if request.POST.get('text'):
        places = places.filter(translations__name__istartswith=request.POST.get('q'))
    if request.POST.get('city'):
        places = places.filter(city__pk=request.POST.get('city'))
    
    return HttpResponse(json(places[:20], ['name']), mimetype="text/javascript")
