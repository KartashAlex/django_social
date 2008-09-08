from django.db import models
from django.utils.translation import ugettext_lazy as _

class Country(models.Model):
    name = models.CharField(maxlength=255)
    
    def __unicode__(self):
        return self.name

class City(models.Model):
    country = models.ForeignKey(Country)
    name = models.CharField(maxlength=255)
    
    class Meta:
        ordering = ('country__name', 'name')
    
    def __unicode__(self):
        return u'%s - %s' % (self.country.name, self.name)
