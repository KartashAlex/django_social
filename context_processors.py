import os.path

from django.conf import settings
from django.shortcuts import get_object_or_404
from net.models import User, Event

def common(request):
    return {
        'request': request,
        'settings': settings,
        }


def widgets(request, user=None):
    from django.db.models import ObjectDoesNotExist
    from photo.models import Photo, User
    try:
        events_owner = request.user.user
        friends = events_owner.get_friends()
        events = Event.objects.filter(from_user=events_owner)
        events = events | Event.objects.filter(user=events_owner)
        events = events | Event.objects.filter(user__in=friends)
        events = events | Event.objects.filter(group__in=events_owner.user_groups.all())
        events = events.order_by('-sent')[:10]
    except (User.DoesNotExist, AttributeError):
        events = []
    
    try:
        user = user or request.user.user
        posts = user.posts.filter(type='blog')
        ads = user.posts.filter(type='ads')
        return {
                'widgets': {
                    'profile': user,
                    'events': events,
                    'wall': user.get_messages()[:3],
                    'messages' : user.get_private_messages()[:3],
                    'wall_count': user.get_messages().count() - 3 if user.get_messages().count() > 3 else 0,
                    'messages_count' : user.get_private_messages().count() - 3 if user.get_private_messages().count() > 3 else 0,
                    'photos': Photo.objects.filter(album__user=user).order_by('-added')[:5],
                    'blog': {
                        'posts': posts.order_by('-added')[:2],
                        'ads': ads.order_by('-added')[:1],
                        'posts_count': posts.count() - 2 if posts.count() > 2 else 0,
                        'ads_count': ads.count() - 2 if ads.count() > 1 else 0,
                    },
                    'friends': {
                        'friends_list': user.get_friends()[:5],
                        'friends_count': user.get_friends().count(),
                        'friends_of_count': user.get_friend_of().count(),
                    },
                }
            }
    except (ObjectDoesNotExist, AttributeError, User.DoesNotExist), e:
        return {'widgets': None}

