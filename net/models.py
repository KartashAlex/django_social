# -*- coding: UTF-8 -*-

from django.db import models
from django.contrib.auth.models import User as DjangoUser
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.template.loader import render_to_string
    
import re

import multilingual

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
    'Менеджер пользователей'
    def search(self, field, value):
        'Поиск пользователей'
        return self.filter(**{field + '__icontains': value})

class User(DjangoUser):
    'Класс наследник от пользователя django, содержит дополнительные поля для профиля пользователя '
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
        'Возвращает список людей у которых я в друзьях'
        return User.objects.filter(friends__friend=self)
        
    def get_friends(self):
        'Возвращает список друзей пользователя'
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
        'Возвращает абсолютную ссылку на профиль'
        return reverse('user_profile', args=[self.pk,])

    def get_data(self, field):
        'Возвращает данные о пользователя'
        try:
            return eval(self.__getattribute__(field))
        except (ValueError, SyntaxError):
            return {}
            
    def get_contacts(self):
        'Возвращает контактные данные'
        return self.get_data('contacts')
        
    def get_interests(self):
        'Возвращает интересы пользователя'
        return [interest.strip() for interest in self.interest.split(',')]

    def set_data(self, field, data):
        self.__setattr__(field, u'%s' % data)
        
    def get_all_messages(self):
        'Возвращает все сообщения пользователя'
        from wall.models import Message
        user_ct = ContentType.objects.get_for_model(User)
        return Message.objects.filter(from_user=self)|Message.objects.filter(content_type=user_ct, object_id=self.pk)
        
    def get_messages(self):
        'Возвращает сообщения на стенку'
        return self.get_all_messages().filter(private=False)
        
    def get_private_messages(self):
        'Возвращает личные сообщения'
        return self.get_all_messages().filter(private=True)
        
    def get_name(self):
        'Возвращает имя пользователя'
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
    'Тип места -- университет/школа/etc'
    class Translation(multilingual.Translation):
        name = models.CharField(_('Name'), max_length=255)
     
    def __unicode__(self):
        return self.name_ru
     
class PlaceTemplate(models.Model):
    type = models.ForeignKey(PlaceType)
               
    city = models.ForeignKey(City, blank=True, null=True)
    map_link = models.URLField(blank=True, null=True)
    
    class Translation(multilingual.Translation):
        name = models.CharField(_('Name'), max_length=255)
        address = models.TextField(blank=True, null=True)

     
    def __unicode__(self):
        return self.name or _(u'Place %s') % self.pk
    
class Place(models.Model):
    'Модель мест -- университетов, городов, школ, мест работы и так далее'
    user = models.ForeignKey(User, related_name='places')
    template = models.ForeignKey(PlaceTemplate, related_name='places')
    
    from_date = models.DateField(blank=True, null=True)
    to_date = models.DateField(blank=True, null=True)
    
class NetGroup(models.Model):
    'Модель группы'
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    interest = models.TextField(_('Favorite interests'), blank=True, default='')
    
    owner = models.ForeignKey(User, related_name='owner_groups')
    admins = models.ManyToManyField(User, related_name='admin_groups', blank=True, editable=False)
    members = models.ManyToManyField(User, related_name='user_groups', blank=True, editable=False)
    
    class UserException(Exception):
        pass
    
    def __unicode__(self):
        return self.name or _(u'Group %s') % self.pk
        
    def get_absolute_url(self):
        return reverse('groups_profile', args=[self.pk])
    
    def get_interests(self):
        return [interest.strip() for interest in self.interest.split(',')]

    def save(self, *args, **kwargs):
        super(NetGroup, self).save(*args, **kwargs)
        self.update_users()
    
    def get_photos(self):
        from photo.models import Photo
        return Photo.objects.filter(album__group=self)
    
    def add_admin(self, user):
        self.admins.add(user)
        self.save()

    def remove_admin(self, user):
        self.admins.remove(user)
        self.save()

    def remove_user(self, user):
        from signals import removed_from_group
        if user == self.owner:
            raise NetGroup.UserException('Cannot delete Owner from Group.')
        self.members.remove(user)
        if user in self.admins.all():
            self.admins.remove(user)
        removed_from_group.send(sender=self.__class__, group=self, user=user)
    
    def add_user(self, user):
        from signals import added_to_group
        self.members.add(user)
        added_to_group.send(sender=self.__class__, group=self, user=user)
    
    def members_count(self):
        return self.members.all().count()

    def update_users(self):
        if not self.owner in self.admins.all():
            self.add_admin(self.owner)
        for admin in self.admins.all():
            if not admin in self.members.all():
                self.add_user(admin)

    def admins_list(self):
        return ', '.join([a.get_name() for a in self.admins.all()])

# events processing

class EventManager(models.Manager):
    def create_event(self, sender, user=None, type='event', group=None, extra={}, msg=''):
        if not msg:
            site = Site.objects.get_current()
            extra.update({'site': site, 'sender': sender, 'user': user, 'group': group})
            msg = render_to_string('emails/%s.txt' % (type), extra)

        return self.create(from_user=sender, user=user, body=msg, type=type, group=group)

class Event(models.Model):
    from_user = models.ForeignKey(User, related_name='events_out', verbose_name=_('Generator'))
    user = models.ForeignKey(User, related_name='events_in', verbose_name=_('Respondent'), blank=True, null=True)
    group = models.ForeignKey(NetGroup, related_name='events_in', verbose_name=_('Group'), blank=True, null=True)
    
    body = models.TextField(_('Body'))
    type = models.CharField(_('Type'), max_length=255, editable=False)
    sent = models.DateTimeField(_('Sent time'), auto_now_add=True)
    
    objects = EventManager()
    
    def get_address(self):
        return self.user or self.group
        
    def get_body(self, user):
        if user.is_authenticated():
            site = Site.objects.get_current()
            extra = {'site': site, 'sender': self.from_user, 'user': self.user, 'group': self.group}
            if self.user.pk == user.pk:
                return render_to_string('emails/to_me/%s.txt' % (self.type), extra)
            elif self.from_user.pk == user.pk:
                return render_to_string('emails/my/%s.txt' % (self.type), extra)
        return self.body
            

