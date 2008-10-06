from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('wall.views',
    (r'^(\d+)/$', 'messages', {'type': 'wall'}, 'wall'),
    (r'^wall/$', 'messages', {'type': 'wall'}, 'my_wall'),
    (r'^all/$', 'messages', {'type': 'all'}, 'my_history'),
    (r'^inbox/$', 'messages', {'type': 'inbox'}, 'inbox'),
    (r'^outbox/$', 'messages', {'type': 'outbox'}, 'outbox'),
    (r'^(\d+)/new/$', 'create_pm', {}, 'create_pm'),
)

