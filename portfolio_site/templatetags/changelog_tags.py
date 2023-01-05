from django import template
from django.utils.html import format_html
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def added():
    return mark_safe('<div class="change-tag change-tag-added">added</div>')


class VersionTag(template.Node):
    def __init__(self, inner_nodes, version: str):
        self.version = version
        self.inner_nodes = inner_nodes

    def render(self, context):
        return format_html('''
            <a id="{}" href="#{}">Version {}</a>
            <div class="changelog-item" data-version="{}">
                {}
            </div>
        ''', self.version, self.version, self.version, self.version,
                           mark_safe(self.inner_nodes.render(context)))


@register.tag(name='version')
def parse_version_tag(parser, token):
    tag_name, version = token.contents.split(None, 1)
    inner_nodes = parser.parse(('endversion',))
    parser.delete_first_token()
    return VersionTag(inner_nodes, version)

