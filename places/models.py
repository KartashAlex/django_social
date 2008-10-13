from django.db import models
from django.utils.translation import ugettext_lazy as _

class Country(models.Model):
    name = models.CharField(max_length=255)
    
    def __unicode__(self):
        return self.name

class City(models.Model):
    country = models.ForeignKey(Country)
    name = models.CharField(max_length=255)
    
    class Meta:
        ordering = ('country__name', 'name')
    
    def __unicode__(self):
        return self.name
