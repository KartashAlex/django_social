from django.conf.urls.defaults import *

urlpatterns = patterns('blog.views',
    (r'^add/(\w+)/$', 'add', {}, 'post_add'),
    (r'^(\d+)/(\w+)/$', 'list', {}, 'post_list'),
    (r'^(\d+)/(\w+)/(\d+)/$', 'profile', {}, 'post_profile'),
)
