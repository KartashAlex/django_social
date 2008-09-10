import os.path

from django.conf import settings

def common(request):
    return {
        'request': request,
        'settings': settings,
        }

def widgets(request):
    from django.db.models import ObjectDoesNotExist
    from photo.models import Photo
    try:
        user = request.user.user
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

