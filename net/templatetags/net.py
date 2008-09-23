from django import template
from django.conf import settings

register = template.Library()

class IfInNode(template.Node):
    def __init__(self, var1, var2, nodelist_true, nodelist_false):
        self.var1, self.var2 = template.Variable(var1), template.Variable(var2)
        self.nodelist_true, self.nodelist_false = nodelist_true, nodelist_false

    def __repr__(self):
        return "<IfInNode>"

    def render(self, context):
        try:
            val1 = self.var1.resolve(context)
        except template.VariableDoesNotExist:
            val1 = None
        try:
            val2 = self.var2.resolve(context)
        except template.VariableDoesNotExist:
            val2 = None
        if val1 in val2:
            return self.nodelist_true.render(context)
        return self.nodelist_false.render(context)
        
#@register.tag
def ifin(parser, token):
    bits = list(token.split_contents())
    if len(bits) != 3:
        raise template.TemplateSyntaxError, "%r takes two arguments" % bits[0]
    end_tag = 'end' + bits[0]
    nodelist_true = parser.parse(('else', end_tag))
    token = parser.next_token()
    if token.contents == 'else':
        nodelist_false = parser.parse((end_tag,))
        parser.delete_first_token()
    else:
        nodelist_false = template.NodeList()
    return IfInNode(bits[1], bits[2], nodelist_true, nodelist_false)
ifin = register.tag(ifin)
