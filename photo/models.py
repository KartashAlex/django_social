from django.db import models

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

class Photo(models.Model):
    album = models.ForeignKey(Album, related_name='photos')
    title = models.CharField(max_length=255, blank=True, default='')
    image = models.ImageField(upload_to='albums/%Y/%m/%d/')
    added = models.DateTimeField(auto_now_add=True, null=True)
    
    class Admin:
        pass
    
    def __unicode__(self):
        return self.title
