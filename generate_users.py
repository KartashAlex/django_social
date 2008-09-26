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

from django.core.files.base import ContentFile
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO


from net.models import User

for i in range(1, 1000):
    username = ''.join([str(random.randint(1, 9)) for j in range(0,8)])
    u = User.objects.create(username=username, email='%s@example.com' % username)
    u.set_password('test')
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
