from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from net.models import User

class AdCategory(models.Model):
    name = models.CharField(_('Name'), max_length=255)

class Post(models.Model):
    TYPES = (
        ('blog', _('Blog post')),
        ('ads', _('Advertisement')),
    )

    author = models.ForeignKey(User, verbose_name=_('Author'), related_name='posts')
    type = models.CharField(_('Type'), max_length=32, choices=TYPES)
    subject = models.CharField(_('Subject'), max_length=255)
    text = models.TextField()
    added = models.DateTimeField(auto_now_add=True, blank=True)
    ad_cat = models.ForeignKey(AdCategory, verbose_name=_('Ad category'), null=True, blank=True)
    
    def get_absolute_url(self):
        return reverse('post_profile', args=[self.author.pk, self.type, self.pk])

    def get_type(self):
        return [t[1] for t in self.TYPES if t[0] == self.type][0] 
