import os.path

from django.conf import settings
from django.shortcuts import get_object_or_404
from net.models import User

def common(request):
    return {
        'request': request,
        'settings': settings,
        }


def widgets(request, user=None):
    from django.db.models import ObjectDoesNotExist
    from photo.models import Photo
    try:
        user = user or request.user.user
        posts = user.posts.filter(type='blog')
        ads = user.posts.filter(type='ads')
        return {
                'widgets': {
                    'wall': user.get_messages()[:3],
                    'photos': Photo.objects.filter(album__user=user).order_by('-added')[:5],
                    'blog': {
                        'posts': posts.order_by('-added')[:2],
                        'ads': ads.order_by('-added')[:1],
                        'posts_count': posts.count() if posts.count() > 2 else 0,
                        'ads_count': ads.count() if ads.count() > 1 else 0,
                    }
                }
            }
    except (ObjectDoesNotExist, AttributeError), e:
        print e
        return {'widgets': None}

