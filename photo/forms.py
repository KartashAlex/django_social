from django import forms
from django.contrib.contenttypes.models import ContentType

from models import Album, Photo

class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['title', ]
        
    def save(self, user, *args, **kwargs):
        msg = super(AlbumForm, self).save(commit=False, *args, **kwargs)
        msg.user = user
        msg.save()
        return msg

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image', 'title']
        
    def __init__(self, album=None, *args, **kwargs):
        self.album = album
        super(PhotoForm, self).__init__(*args, **kwargs)
        
    def save(self, *args, **kwargs):
        msg = super(PhotoForm, self).save(commit=False, *args, **kwargs)
        msg.album = self.album
        if not msg.title:
            msg.title = msg.image
        msg.save()
        return msg
