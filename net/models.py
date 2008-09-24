# -*- coding: UTF-8 -*-

from django.db import models
from django.contrib.auth.models import User as DjangoUser
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse

import re

from places.models import City, Country

USERDATA_TYPES = (
    ('interest', _('Interest')),
    ('writer', _('Writer')),
    ('site', _('Site')),
    ('private', _('Other favorite')),
)

class UserData(models.Model):
    type = models.CharField(max_length=15, choices=USERDATA_TYPES)
    title = models.CharField(max_length=511)
    
    class Meta:
        ordering=['title']
        
    class Admin:
        pass
    
    def __unicode__(self):
        return u'%s %s' % (self.type, self.title)

GENDER_CHOICES = (
    ('male', _('Male')),
    ('female', _('Female')),
)

TAG_FIELDS = ['writer', 'site', 'private', ]
DATA_FIELDS = {
    'contacts': ['phone', 'icq', 'skype', 'jabber', 'msn'],
}

DjangoUser._meta.get_field('username').validator_list = []
DjangoUser._meta.get_field('username').help_text = ''

class UserManager(models.Manager):
    def search(self, field, value):
        return self.filter(**{field + '__icontains': value})

class User(DjangoUser):
    
    # Common information
    
    avatar = models.ImageField(_('Avatar'), upload_to='avatars/%Y/%m/', blank=True, null=True)
    country = models.ForeignKey(Country, verbose_name=_('Country'), blank=True, null=True)
    city = models.ForeignKey(City, verbose_name=_('City'), blank=True, null=True)
    birthdate = models.DateField(_('Birthdate'), blank=True, null=True)
    gender = models.CharField(_('Gender'), max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    about = models.TextField(_('About me'), blank=True, default='')

    # Contacts

    contacts = models.TextField(_('Other contacts'), blank=True, default='')

    # Private info

    interest = models.TextField(_('Favorite interests'), blank=True, default='')
    writer = models.TextField(_('Favorite writers'), blank=True, default='')
    site = models.TextField(_('Favorite sites'), blank=True, default='')
    private = models.TextField(_('Other favorites'), blank=True, default='')

    # Work info
    
    user_data = models.ManyToManyField(UserData, blank=True, null=True, editable=False)

    objects = UserManager()

    class Admin:
        pass
        
    def get_friend_of(self):
        return User.objects.filter(friends__friend=self)
        
    def get_friends(self):
        return User.objects.filter(friend_of__friend_of=self)
        
    def save(self, *args, **kwargs):
        if self.pk:
            for key in TAG_FIELDS:
                data_str = set([d.strip() for d in self.__getattribute__(key).split(',')])
                user_data_list = self.user_data.filter(type__exact=key)
                user_data_str = set([ud.title for ud in user_data_list])
                if data_str != user_data_str:
                    user_data_list.filter(title__in=user_data_str-data_str).delete()
                    for title in data_str-user_data_str:
                        if title.strip() != '':
                            data, created = UserData.objects.get_or_create(type=key, title=title)
                            self.user_data.add(data)
                        
        super(User, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('user_profile', args=[self.pk,])

    def get_data(self, field):
        try:
            return eval(self.__getattribute__(field))
        except (ValueError, SyntaxError):
            return {}
            
    def get_contacts(self):
        return self.get_data('contacts')
        
    def get_interests(self):
        return [interest.strip() for interest in self.interest.split(',')]

    def set_data(self, field, data):
        self.__setattr__(field, u'%s' % data)
        
    def get_all_messages(self):
        from wall.models import Message
        user_ct = ContentType.objects.get_for_model(User)
        return Message.objects.filter(from_user=self)|Message.objects.filter(content_type=user_ct, object_id=self.pk)
        
    def get_messages(self):
        return self.get_all_messages().filter(private=False)
        
    def get_private_messages(self):
        return self.get_all_messages().filter(private=True)
        
    def get_name(self):
        if self.first_name or self.last_name:
            return u'%s %s' % (self.first_name, self.last_name)
        try:
            return re.findall('[^@]*', self.username)[0]
        except IndexError:
            return u'User %s' % self.pk
        
class Friend(models.Model):
    friend = models.ForeignKey(User, related_name='friend_of')
    friend_of = models.ForeignKey(User, related_name='friends')
        
class PlaceType(models.Model):
    name = models.CharField(max_length=255)
     
    def __unicode__(self):
        return self.name
               
class Place(models.Model):
    user = models.ForeignKey(User, related_name='places')
    type = models.ForeignKey(PlaceType)
    
    name = models.CharField(max_length=255)
    city = models.ForeignKey(City, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    map_link = models.URLField(blank=True, null=True)
    
    from_date = models.DateField(blank=True, null=True)
    to_date = models.DateField(blank=True, null=True)
    
    def __unicode__(self):
        return self.name
