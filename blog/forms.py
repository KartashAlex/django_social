from django import forms

from models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['author']

    def save(self, user):
        post = super(PostForm, self).save(commit=False)
        post.author = user
        post.save()
        
        return post
