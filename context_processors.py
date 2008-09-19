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
        return {
                'widgets': {
                    'wall': user.get_messages()[:3],
                    'photos': Photo.objects.filter(album__user=user).order_by('-added')[:5],
                    'blog': {
                        'posts': user.posts.filter(is_ad=False).order_by('-added')[:2],
                        'ads': user.posts.filter(is_ad=True).order_by('-added')[:1],
                    }
                }
            }
    except (ObjectDoesNotExist, AttributeError):
        return {}

