# -*- coding: UTF-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _

from net.models import User

class Album(models.Model):
    user = models.ForeignKey(User, related_name='albums')
    title = models.CharField(max_length=255)
    
    class Admin:
        pass
	
    def random_img(self):
        images = self.photos.all().order_by('?')
        try:
            return images[0]
        except IndexError:
            return None
    
    def __unicode__(self):
        return self.title
        
    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('photos', args=[self.user.pk, self.pk])

class Photo(models.Model):
    album = models.ForeignKey(Album, related_name='photos')
    title = models.CharField(max_length=255, blank=True, default='')
    image = models.ImageField(upload_to='albums/%Y/%m/%d/')
    added = models.DateTimeField(auto_now_add=True, null=True)
    
    class Admin:
        pass
    
    def __unicode__(self):
        return self.title
        
    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('photo', args=[self.album.user.pk, self.album.pk, self.pk])
