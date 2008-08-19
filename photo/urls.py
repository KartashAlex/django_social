from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('photo.views',
    (r'^(\d+)/$', 'albums', {}, 'albums'),
    (r'^add/$', 'create_album', {}, 'create_album'),
    (r'^(\d+)/(\d+)/$', 'photos', {}, 'photos'),
    (r'^(\d+)/(\d+)/add/$', 'create_photo', {}, 'create_photo'),
    (r'^(\d+)/(\d+)/(\d+)/$', 'photo', {}, 'photo'),
)

