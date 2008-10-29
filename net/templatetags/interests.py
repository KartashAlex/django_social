# -*- coding:utf-8 -*-
from django import template
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from django.db.models import get_models, get_model
from django.utils.encoding import smart_str, force_unicode
from django.utils.safestring import mark_safe
from django.conf import settings

register = template.Library()

class ListNode(template.Node):
    def __init__(self, list_var, type):
        self.list_var, self.type = list_var, type

    def render(self, context):
        list_str = template.Variable(self.list_var).resolve(context)
        
        return ''.join(['<li><a href="/search/?%s=%s">%s</a></li>' % (self.type, s.strip(), s.strip()) for s in list_str.split(',')])
        
def interests(parser, token):
    tokens = token.contents.split()
    if len(tokens) != 3:
        raise template.TemplateSyntaxError, "'%s' tag requires 2 arguments" % tokens[0]
    return ListNode(*tokens[1:])
register.tag('interests', interests)
