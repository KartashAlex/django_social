# -*- coding: UTF-8 -*-

from django import forms
from django.contrib.contenttypes.models import ContentType
from django.forms import formsets
from django.utils.translation import ugettext_lazy as _

from models import Album, Photo

class AlbumForm(forms.ModelForm):
    album = forms.ChoiceField()
    class Meta:
        model = Album
        fields = ['title']

    def __init__(self, album_id=None, user=None, *args, **kwargs):
        self.user = user
        super(AlbumForm, self).__init__(*args, **kwargs)
        self.fields['album'].choices=[(a.pk, a.title) for a in Album.objects.filter(user=self.user)]
        self.fields['album'].initial = album_id
        self.fields['album'].required = False
        self.fields['title'].label = _(u'Новый альбом')
        self.fields['title'].required = False

    def clean_album(self):
        if self.cleaned_data['title']:
            album = Album.objects.create(title=self.cleaned_data['title'], user=self.user)
            return album.pk
        if self.cleaned_data['album']:
            return self.cleaned_data['album']
        raise forms.ValidationError(_('Album is required.'))

    def save(self):
        return Album.objects.get(pk=self.cleaned_data['album'])
            
class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['album', 'title', 'image']
        
    def __init__(self, *args, **kwargs):
        self.album = None
        super(PhotoForm, self).__init__(*args, **kwargs)
        self.fields['album'].widget = forms.HiddenInput()
        self.fields['album'].required = False
    
    def clean_album(self):
        if self.album:
            return self.album
    
    def save(self, *args, **kwargs):
        photo = super(PhotoForm, self).save(commit=False)
        if photo.image:
            if not photo.title:
                photo.title = unicode(photo.image)
            photo.save()
            return photo

# PhotoFormSet = formsets.formset_factory(PhotoForm, extra=5)
class PhotoFormSet(formsets.BaseFormSet):
    form = PhotoForm
    extra = 5
    max_num = 5
    can_order = False
    can_delete = False

    def __init__(self, album=None, *args, **kwargs):
        self.album = album
        super(PhotoFormSet, self).__init__(*args, **kwargs)
        for form in self.forms:
            form.album = self.album
