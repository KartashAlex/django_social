from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType

from net.models import User

class Message(models.Model):
    from_user = models.ForeignKey(User, related_name='messages', verbose_name=_('From'))
    
    body = models.TextField(_('Body'))
    
    private = models.BooleanField(_('Private'), default=False)
    sent = models.DateTimeField(_('Sent time'), auto_now_add=True)
    
    parent = models.ForeignKey('self', related_name='children', verbose_name=_('Parent'), blank=True, null=True)
    content_type = models.ForeignKey(ContentType)
    object_id = models.IntegerField(_('object ID'))

    def get_address(self):
        return self.content_type.get_object_for_this_type(pk=self.object_id)
