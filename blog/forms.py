from django import forms
from django.utils.translation import ugettext_lazy as _

from models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['author', 'type']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        try:
            self.type = kwargs.pop('type')
        except:
            self.type = "blog"
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['group'].choices = [('', _('None'))] + [(g.id, g.name) for g in self.user.user_groups.all()]
        if not self.fields['group'].choices:
            self.fields['group'].widget = forms.HiddenInput()
        if self.type == "blog":
            self.fields['ad_cat'].widget = forms.HiddenInput()

    def save(self):
        post = super(PostForm, self).save(commit=False)
        post.author = self.user

        post.type = self.type
        post.save()
        
        return post
