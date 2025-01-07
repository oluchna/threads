from django import template
import re

register = template.Library()

@register.filter
def remove_images(content):
    return re.sub(r'<img[^>]*>', '', content)

@register.filter(name='remove_html')
def remove_html_tags(content):
    print(isinstance(content, str))
    if isinstance(content, str):
        return re.sub(r'<.*?>', '', content)
    return content