# -*- coding:utf-8 -*-
from django import template
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from django.db.models import get_models, get_model
from django.utils.encoding import smart_str, force_unicode
from django.utils.safestring import mark_safe
from django.conf import settings
from django.template.defaultfilters import stringfilter

register = template.Library()

class WallForm(template.Node):
    def __init__(self, form, method, *param):
        self.form, self.method, self.param = form, method, param

    def render(self, context):
        form = template.Variable(self.form).resolve(context)
        param = [template.Variable(p).resolve(context) for p in self.param]
        return form.__getattribute__(self.method)(*param)
        
def wall_form(parser, token):
    tokens = token.contents.split()
    if len(tokens) < 2:
        raise template.TemplateSyntaxError, "'%s' tag requires one arguments" % tokens[0]
    return WallForm(*tokens[1:])
register.tag('wall_form', wall_form)
