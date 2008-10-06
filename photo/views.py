from django.views.generic import list_detail
from django.contrib.auth.decorators import login_required
from decorators import render_to
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404

from forms import AlbumForm, PhotoFormSet
from models import Album, Photo

def albums(request, user_id):
    kwargs = {
        'queryset': Album.objects.filter(user__pk=user_id),
        'template_name': 'photo_albums.html',
        'paginate_by': 15,
        'extra_context': {
            'username': user_id,
        },
    }
    return list_detail.object_list(request, **kwargs)

def photos(request, user_id, album_id):
    try:
        user_id = int(user_id)
    except:
        return Http404
    album = get_object_or_404(Album, pk=album_id, user__pk=user_id)
    kwargs = {
        'queryset': Photo.objects.filter(album=album),
        'template_name': 'photo_photos.html',
        'paginate_by': 14,
        'extra_context': {
            'username': user_id,
            'album': album,
        },
    }
    return list_detail.object_list(request, **kwargs)

def photo(request, user_id, album_id, photo_id):
    kwargs = {
        'queryset': Photo.objects.filter(album__user__pk=user_id, album__id=album_id),
        'object_id': photo_id,
        'template_name': 'photo_photo.html',
        'extra_context': {
            'username': user_id,
        },
    }
    return list_detail.object_detail(request, **kwargs)

@login_required
@render_to('photo_create.html')
def create_photo(request):
    if request.POST:
        album_form = AlbumForm(album_id=request.REQUEST.get('album_id'), user=request.user.user, data=request.POST)
        if album_form.is_valid():
            album = album_form.save()
        else:
            album = None
            
        photo_formset = PhotoFormSet(album, request.POST, request.FILES)
        if album and photo_formset.is_valid():
            for form in photo_formset.forms:
                if form.is_valid():
                    form.save()
            return HttpResponseRedirect('/me')
    else:
        album_form = AlbumForm(album_id=request.REQUEST.get('album_id'), user=request.user.user)
        photo_formset = PhotoFormSet()
    return {
        'album_form': album_form,
        'photo_forms': photo_formset,
    }
