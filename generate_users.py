#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os, sys

project_directory = os.path.dirname(os.path.abspath(__file__))
project_name = os.path.basename(project_directory)
sys.path.append(os.path.join(project_directory, '..'))
project_module = __import__(project_name, '', '', [''])
sys.path.pop()
os.environ['DJANGO_SETTINGS_MODULE'] = '%s.settings' % project_name

import math, random
from PIL import Image, ImageDraw
from datetime import datetime, timedelta

from django.core.files.base import ContentFile
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO


from net.models import User, Country, City

letters = (ord('a'), ord('z'))
interests = u'рыбалка, спорт, путешествия, развлечения, игры, пейнтбол, чтение, футбол, кино, море'.split(', ')

User.objects.filter(is_superuser=False).delete()

def random_name(length):
    return ''.join([chr(random.randint(*letters)) for j in range(0, length)])

for i in range(1, 1000):
    username = random_name(8)
    u = User.objects.create(username=username, email='%s@example.com' % username)
    u.set_password('test')
    u.first_name = random_name(12).title()
    u.last_name = random_name(15).title()
    u.country = Country.objects.all().order_by('?')[0]
    u.city = City.objects.filter(country__pk=u.country.pk).order_by('?')[0]
    u.birthdate = datetime.now() - timedelta(random.randint(5000, 20000))
    u.interest = ', '.join(random.sample(interests, 3))
    u.save()
    
    im = Image.new('RGB', (200,150)) # create the image
    draw = ImageDraw.Draw(im)   # create a drawing object that is
                                # used to draw on the new image
    red = (255,0,0)    # color of our text
    text_pos = (10,10) # top-left position of our text
    draw.text(text_pos, str(i), fill=red)
    
    del draw # I'm done drawing so I don't need this anymore
    
    s = StringIO()
    im.save(s, 'png')
    u.avatar.save('%s.png' % i, ContentFile(s.getvalue()))
    u.save()
