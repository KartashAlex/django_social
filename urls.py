from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin

for app in settings.OUR_APPS:
    try:
        __import__("%s.admin" % app)
    except ImportError:
        pass
        
urlpatterns = patterns('',
    ('^admin/(.*)', admin.site.root),
    (r'^i18n/', include('django.conf.urls.i18n')),
    (r'^accounts/', include('django_registration.urls')),
    (r'^msg/', include('wall.urls')),
    
    (r'^', include('net.urls')),
    (r'^photos/', include('photo.urls')),

    # Media for debugging
    (r'^%s(?P<path>.*)$' % (settings.MEDIA_URL[1:]), 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}), 
)

# TODO
# pseudo-"generic" to output queryset or object as json
# urls for contrib
# views for contrib info
