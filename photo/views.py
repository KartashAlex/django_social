from django.views.generic import list_detail
from django.contrib.auth.decorators import login_required
from decorators import render_to
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from forms import AlbumForm, PhotoForm
from models import Album, Photo

def albums(request, user_id):
    kwargs = {
        'queryset': Album.objects.filter(user__pk=user_id),
        'template_name': 'photo_albums.html',
        'extra_context': {
            'username': user_id,
        },
    }
    return list_detail.object_list(request, **kwargs)

def photos(request, user_id, album_id):
    from forms import PhotoForm
    form = PhotoForm()
    album = get_object_or_404(Album, pk=album_id, user__pk=user_id)
    kwargs = {
        'queryset': Photo.objects.filter(album=album),
        'template_name': 'photo_photos.html',
        'extra_context': {
            'username': user_id,
            'form': form,
            'album': album,
        },
    }
    return list_detail.object_list(request, **kwargs)

def photo(request, user_id, album_id, photo_id):
    username = username.replace('*', '@')
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
@render_to('album_create.html')
def create_album(request):
    if request.POST:
        form = AlbumForm(data=request.POST)
        if form.is_valid():
            album = form.save(request.user.user)
            return HttpResponseRedirect(reverse('photos', args=[album.user.pk, album.pk]))
    else:
        form = AlbumForm()
    return {
        'form': form,
    }

@login_required
@render_to('photo_create.html')
def create_photo(request, user_id, album_id):
    album = get_object_or_404(Album, pk=album_id, user__pk=user_id)
    if request.POST:
        form = PhotoForm(data=request.POST, files=request.FILES, album=album)
        if form.is_valid():
            album = form.save().album
            return HttpResponseRedirect(reverse('photos', args=[album.user.pk, album.pk]))
    else:
        form = PhotoForm()
    return {
        'form': form,
    }
