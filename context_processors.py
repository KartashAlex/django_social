import os.path

from django.conf import settings

def common(request):
    return {
        'request': request,
        'settings': settings,
        }

