from django import forms
from django.utils.translation import ugettext_lazy as _

from models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['author']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['group'].choices = [('', _('None'))] + [(g.id, g.name) for g in self.user.user_groups.all()]
        if not self.fields['group'].choices:
            self.fields['group'].widget = forms.HiddenInput()

    def save(self):
        post = super(PostForm, self).save(commit=False)
        post.author = self.user
        post.save()
        
        return post
