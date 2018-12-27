from django import template

from components import LinkNode, ValueNode

register = template.Library()


@register.filter
def is_link_node(node):
    return isinstance(node, LinkNode)


@register.filter
def is_value_node(node):
    return isinstance(node, ValueNode)
