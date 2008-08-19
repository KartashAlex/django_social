# -*- coding: utf8 -*-

from django.db import models
from django.contrib.auth.models import User as DjangoUser
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType

from places.models import City, Country

USERDATA_TYPES = (
    ('interest', _('Interest')),
    ('writer', _('Writer')),
    ('site', _('Site')),
    ('private', _('Other favorite')),
    
    ('school', _('School')),
    ('university', _('University')),
    ('work', _('Workplace')),
    ('professional', _('Professional data')),
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
    ('male', _(u'Male')),
    ('female', _(u'Female')),
)

TAG_FIELDS = ['writer', 'site', 'private', 'school', 'university', 'work', 'professional']
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
    
    avatar = models.ImageField(_(u'Аватар'), upload_to='avatars/%Y/%m/', blank=True, null=True)
    country = models.ForeignKey(Country, verbose_name=_(u'Страна'), blank=True, null=True)
    city = models.ForeignKey(City, verbose_name=_(u'Город проживания'), blank=True, null=True)
    birthdate = models.DateField(_(u'Дата рождения'), blank=True, null=True)
    gender = models.CharField(_(u'Пол'), max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    politics = models.TextField(_('Political position'), blank=True, default='')
    about = models.TextField(_('About me'), blank=True, default='')

    # Contacts

    contacts = models.TextField(_('Other contacts'), blank=True, default='')

    # Private info

    interest = models.TextField(_('Favorite interests'), blank=True, default='')
    writer = models.TextField(_('Favorite writers'), blank=True, default='')
    site = models.TextField(_('Favorite sites'), blank=True, default='')
    private = models.TextField(_('Other favorites'), blank=True, default='')

    # Work info
    
    school = models.CharField(_('My school'), max_length=200, blank=True, default='')
    university = models.CharField(_('My university'), max_length=200, blank=True, default='')
    work = models.CharField(_('My working place'), max_length=200, blank=True, default='')
    professional = models.CharField(_('Other professional data'), max_length=200, blank=True, default='')

    user_data = models.ManyToManyField(UserData, blank=True, null=True, editable=False)

    objects = UserManager()

    class Admin:
        pass
        
    def save(self):
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
                        
        super(User, self).save()

    def get_data(self, field):
        try:
            return eval(self.__getattribute__(field))
        except (ValueError, SyntaxError):
            return {}
            
    def get_contacts(self):
        return self.get_data('contacts')
        
    def get_schools(self):
        return self.schools.all()
        
    def get_interests(self):
        return [interest.strip() for interest in self.interest.split(',')]

    def set_data(self, field, data):
        self.__setattr__(field, u'%s' % data)
        
    def get_messages(self):
        from wall.models import Message
        user_ct = ContentType.objects.get_for_model(User)
        return Message.objects.filter(from_user=self)|Message.objects.filter(content_type=user_ct, object_id=self.pk)
        
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
