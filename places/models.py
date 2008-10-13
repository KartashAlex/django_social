from django.db import models
from django.utils.translation import ugettext_lazy as _

import multilingual

class Country(models.Model):
    class Translation(multilingual.Translation):
        name = models.CharField(_('Name'), max_length=255)
    
    def __unicode__(self):
        return self.name

class City(models.Model):
    country = models.ForeignKey(Country)
    class Translation(multilingual.Translation):
        name = models.CharField(_('Name'), max_length=255)
    
    def __unicode__(self):
        return self.name
