import base64
from django import template

register = template.Library()

@register.filter
def b64encode(value):
    """Converts binary image data to a Base64-encoded string for display."""
    if value:
        return base64.b64encode(value).decode("utf-8")
    return ""
