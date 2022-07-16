from django import template

register = template.Library()

@register.filter(name='key_lookup')
def key_lookup(myDict, key):
    return myDict[key]