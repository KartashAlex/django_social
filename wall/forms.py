from django import forms
from django.contrib.contenttypes.models import ContentType

from models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['body', 'parent', 'private', 'content_type', 'object_id']
        
    def __init__(self, initials, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        for (key, value) in initials.items():
            self.fields[key].initial = value
            self.fields[key].widget = forms.HiddenInput()
            
    def save(self, user, *args, **kwargs):
        msg = super(MessageForm, self).save(commit=False, *args, **kwargs)
        msg.from_user = user
        msg.save()
        return msg
