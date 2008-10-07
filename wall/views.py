from django.views.generic import list_detail, create_update
from django.contrib.contenttypes.models import ContentType
from django.http import Http404, HttpResponseRedirect
from django.db.models import get_model
from django.contrib.auth.decorators import login_required
from decorators import render_to
from django.core.urlresolvers import reverse

from models import Message, User

def messages(request, id=None, type='wall'):
    messages = Message.objects.all().order_by('-sent')
    user_ct = ContentType.objects.get_for_model(User)
    if type == 'outbox' and request.user.is_authenticated():
        messages = messages.filter(from_user=request.user.user)
    elif type == 'all' and request.user.is_authenticated():
        messages = messages.filter(from_user=request.user.user) | messages.filter(content_type=user_ct, object_id=request.user.user.pk)
    elif type == 'inbox' and request.user.is_authenticated():
        messages = messages.filter(content_type=user_ct)
        if id:
            messages = messages.filter(object_id=id)
        else:
            messages = messages.filter(object_id=request.user.user.pk)
    elif type == 'wall':
        if id:
            messages = messages.filter(private=False, content_type=user_ct, object_id=id)
        else:
            messages = messages.filter(private=False, content_type=user_ct, object_id=request.user.user.pk)
    else:
        return Http404
    kwargs = {
        'queryset': messages,
        'template_name': 'wall_messages.html',
        'paginate_by': 10,
        'extra_context': {
            'msg_type': type,
        },
    }
    return list_detail.object_list(request, **kwargs)

@login_required
@render_to('wall_create.html')
def create_pm(request, id):
    from forms import MessageForm
    model = get_model('net', 'User')
        
    data = {
        'content_type': ContentType.objects.get_for_model(model).pk,
        'object_id': id,
        'parent': request.GET.get('parent'),
        'private': request.GET.get('private'),
    }
    if request.POST:
        form = MessageForm(data=request.POST, initials=data)
        if form.is_valid():
            form.save(request.user.user)
            return HttpResponseRedirect(reverse('user_profile', args=[id]))
    else:
        form = MessageForm(initials=data)
    return {
        'form': form,
        'object_id': id,
    }
