# -*- coding: UTF-8 -*-

from django import forms
from django.contrib.contenttypes.models import ContentType
from django.forms import formsets
from django.utils.translation import ugettext_lazy as _

from models import Album, Photo, NetGroup

class AlbumForm(forms.ModelForm):
    album = forms.ChoiceField()
    class Meta:
        model = Album
        fields = ['title', 'group']

    def __init__(self, album_id=None, user=None, *args, **kwargs):
        self.user = user
        super(AlbumForm, self).__init__(*args, **kwargs)
        self.fields['album'].choices = [(a.pk, a.title) for a in Album.objects.filter(user=self.user, group__isnull=True)]
        self.fields['album'].required = False
        self.fields['title'].label = _(u'Новый альбом')
        self.fields['title'].required = False
        groups_choices = [('g%s' % g.id, _(u'Группа %s') % g.name) for g in self.user.user_groups.all()]
        self.fields['album'].choices += groups_choices
        self.fields['album'].initial = album_id

    def clean_album(self):
        if self.data['title']:
            album = Album.objects.create(title=self.data['title'], user=self.user)
            return album.pk
        if self.cleaned_data['album']:
            return self.cleaned_data['album']
        raise forms.ValidationError(_('Album is required.'))

    def save(self):
        id = self.cleaned_data['album']
        if str(id)[0] != 'g':
            return Album.objects.get(pk=id)
        else:
            group = NetGroup.objects.get(pk=int(str(id)[1:]))
            album, created = Album.objects.get_or_create(
                group=group, 
                user=self.user,
                title=group.name
            )
            return album
            
class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['album', 'image']
        
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
