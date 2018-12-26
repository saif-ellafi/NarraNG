from django import template

from components import LinkNode

register = template.Library()


@register.filter
def is_link_node(node):
    return isinstance(node, LinkNode)
