from django.views.generic import list_detail, create_update
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from models import Post
from forms import PostForm

def list(request, user_id, type, *args, **kwargs):
    kwargs.update({
        'queryset': Post.objects.filter(type=type, author__pk=user_id).order_by('-added'),
        'template_name': 'post_list.html',
        'extra_context': {
            'type': type,
        },
    })
    return list_detail.object_list(request, *args, **kwargs)

def profile(request, user_id, type, id, *args, **kwargs):
    kwargs.update({
        'queryset': Post.objects.filter(type=type, author__pk=user_id),
        'object_id': id,
        'template_name': 'post_profile.html',
        'extra_context': {
            'type': type,
        },
    })
    return list_detail.object_detail(request, *args, **kwargs)

@login_required
def add(request, *args, **kwargs):
    if request.POST:
        form = PostForm(request.POST, user=request.user.user)
        if form.is_valid():
            post = form.save()
            return HttpResponseRedirect(post.get_absolute_url())
    else:
        form = PostForm(user=request.user.user)
    print form
    return render_to_response('post_add.html', {
            'form': form,
        }, context_instance=RequestContext(request))

@login_required
def add_an_ad(request, *args, **kwargs):
    if request.POST:
        form = PostForm(request.POST, user=request.user.user)
        if form.is_valid():
            post = form.save()
            return HttpResponseRedirect(post.get_absolute_url())
    else:
        form = PostForm(user=request.user.user, type="Advertisement")
    print form
    return render_to_response('poast_add.html', {
            'form': form,
        }, context_instance=RequestContext(request))