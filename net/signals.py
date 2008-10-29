# -*- coding: UTF-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.template.loader import render_to_string
from django.db.models import signals
    
import re

from models import Friend, Event, NetGroup

def add_friend(sender, **kwargs):
    friend, friend_of = kwargs['instance'].friend, kwargs['instance'].friend_of
    Event.objects.create_event(sender=friend_of, user=friend, type='friend_add')
signals.post_save.connect(add_friend, sender=Friend)

def delete_friend(sender, **kwargs):
    friend, friend_of = kwargs['instance'].friend, kwargs['instance'].friend_of
    Event.objects.create_event(sender=friend_of, user=friend, type='friend_delete')
signals.pre_delete.connect(delete_friend, sender=Friend)

added_to_group = signals.Signal(providing_args=["group", "user"])
def add_to_group(sender, **kwargs):
    group, user = kwargs['group'], kwargs['user']
    Event.objects.create_event(sender=user, user=user, type='group_add', group=group)
added_to_group.connect(add_to_group, sender=NetGroup)

removed_from_group = signals.Signal(providing_args=["group", "user"])
def remove_from_group(sender, **kwargs):
    group, user = kwargs['group'], kwargs['user']
    Event.objects.create_event(sender=user, user=user, type='group_delete', group=group)
removed_from_group.connect(remove_from_group, sender=NetGroup)
