from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag(takes_context=True)
def footnote(context, footnote_markup: str):
    if 'footnotes' in context:
        context['footnotes'].append(footnote_markup)
    else:
        context['footnotes'] = [footnote_markup]
    
    fn_num = len(context["footnotes"])
    return mark_safe(f'<sup>[<a id="footnote-tag-{fn_num}" href="#footnote-{fn_num}">{fn_num}</a>]</sup>')

@register.simple_tag(takes_context=True)
def footnotes_section(context):
    return mark_safe('<hr><div class="footnotes-container">' + ''.join(f'<p><sup>[<a id="footnote-{i}" href="#footnote-tag-{i}">{i}</a>]</sup><span>{markup}</span></p>' for i, markup in enumerate(context['footnotes'], start=1)) + '</div>')