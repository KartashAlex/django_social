from django import template
from django.conf import settings

register = template.Library()

class MethodNode(template.Node):
    def __init__(self, object, method, *params):
    	self.object = template.Variable(object)
        self.method = template.Variable(method)
        self.args = []
        self.kwargs = {}
        for p in params:
        	try:
        		key, value = p.split('=')
        		self.kwargs[str(key)] = template.Variable(value)
        	except ValueError:
        		self.args.append(template.Variable(p))
         
    def __repr__(self):
        return "<MethodNode>"

    def render(self, context):
    	try:
    		object = self.object.resolve(context)
    	except template.VariableDoesNotExist:
    		object = self.object.var
    	try:
    		method = self.method.resolve(context)
    	except template.VariableDoesNotExist:
    		method = self.method.var
    	args = []
    	for a in self.args:
    		try:
    			args.append(a.resolve(context))
    		except template.VariableDoesNotExist:
    			args.append(a.var)
    	kwargs = {}
    	for k in self.kwargs.keys():
    		try:
    			kwargs[k] = self.kwargs[k].resolve(context)
    		except template.VariableDoesNotExist:
    			kwargs[k] = self.kwargs[k].var
        return object.__getattribute__(method)(*args, **kwargs)
        
@register.tag
def method(parser, token):
	"""
	Calls a method of an object with provided parameters:

		{% object method param0 "param1" param2="test" param3=some_var %}
	"""
	bits = list(token.split_contents())
	return MethodNode(*bits[1:])
