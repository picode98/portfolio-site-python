from django import template
from django.utils.safestring import mark_safe

from os.path import splitext

from typing import Optional, List

register = template.Library()


@register.simple_tag
def web_image(*paths: str, caption: Optional[str] = None):
    caption_markup = "" if caption is None else f'<span class="image-caption">{caption}</span>'

    image_markup = []
    for path in paths:
        if path.endswith(':nopreview'):
            image_markup.append(f'<a href="{path.removesuffix(":nopreview")}" target="_blank"><img src="{path.removesuffix(":nopreview")}"></a>')
        else:
            image_markup.append(f'<a href="{path}" target="_blank"><img src="{splitext(path)[0]}.web.jpg"></a>')

    images = '<div class="image-spacer"></div>'.join(image_markup)

    return mark_safe(f'<div class="web-images"><div class="image-container">{images}</div><p>{caption_markup}</p></div>')