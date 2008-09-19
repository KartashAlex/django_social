from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('photo.views',
    (r'^add/$', 'create_photo', {}, 'create_photo'),
    (r'^(\d+)/$', 'albums', {}, 'albums'),
    (r'^(\d+)/(\d+)/$', 'photos', {}, 'photos'),
    (r'^(\d+)/(\d+)/(\d+)/$', 'photo', {}, 'photo'),
)

