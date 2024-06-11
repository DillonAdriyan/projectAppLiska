# your_app/templatetags/active_tag.py
from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def active(context, pattern):
    import re
    request = context['request']
    if re.search(pattern, request.path):
        return 'tab-active'
    return ''
