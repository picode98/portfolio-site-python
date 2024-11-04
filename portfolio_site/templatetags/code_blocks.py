from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe

import re
from typing import Optional

LANG_KEYWORD_MATCHERS = {
    'C++': re.compile('([^a-zA-Z0-9_])(alignas|alignof|and|and_eq|asm|atomic_cancel|atomic_commit|atomic_noexcept|' +
                      'auto|bitand|bitor|bool|break|case|catch|char|char8_t|char16_t|char32_t|class|compl|' +
                      'concept|const|consteval|constexpr|constinit|const_cast|continue|co_await|co_return|' +
                      'co_yield|decltype|default|delete|do|double|dynamic_cast|else|enum|explicit|export|' +
                      'extern|false|float|for|friend|goto|if|inline|int|long|mutable|namespace|new|noexcept|' +
                      'not|not_eq|nullptr|operator|or|or_eq|private|protected|public|reflexpr|register|' +
                      'reinterpret_cast|requires|return|short|signed|sizeof|static|static_assert|static_cast|' +
                      'struct|switch|synchronized|template|this|thread_local|throw|true|try|typedef|typeid|' +
                      'typename|union|unsigned|using|virtual|void|volatile|wchar_t|while|xor|xor_eq)([^a-zA-Z0-9_])')
}

register = template.Library()

@register.simple_tag
def cs(snippet: str):
    return mark_safe(f'<span class="code-snippet">{escape(snippet)}</span>')

class CodeBlockNode(template.Node):
    def __init__(self, inner_nodes: template.NodeList, highlight_language: Optional[str]):
        self.inner_nodes = inner_nodes
        self.highlight_language = highlight_language.lower()

    def render(self, context):
        content = self.inner_nodes.render(context)
        
        if self.highlight_language == 'c++':
            import cxxheaderparser.lexer
            stream = cxxheaderparser.lexer.LexerTokenStream(None, content)
            stream._discard_types = set()

            new_content = []
            while token := stream.token_eof_ok():
                if token.value in cxxheaderparser.lexer.PlyLexer.keywords:
                    new_content.append(f'<span class="code-keyword">{escape(token.value)}</span>')
                elif token.type in {'COMMENT_SINGLELINE', 'COMMENT_MULTILINE'}:
                    new_content.append(f'<span class="code-comment">{escape(token.value)}</span>')
                else:
                    new_content.append(escape(token.value))
            content = ''.join(new_content)
        else:
            content = escape(content)

            # content = mark_safe(LANG_KEYWORD_MATCHERS[self.highlight_language].sub(
            #     lambda match: f'{match.group(1)}<span class="code-keyword">{match.group(2)}</span>{match.group(3)}',
            # content))

        return f'<pre class="code-block"><code>{content}</code></pre>'

@register.tag
def code_block(parser: template.base.Parser, token: template.base.Token):
    args = token.contents.split(' ')
    language = args[1] if len(args) >= 2 else None
    inner_nodes = parser.parse(('end_code_block',))
    parser.delete_first_token()
    return CodeBlockNode(inner_nodes, language)