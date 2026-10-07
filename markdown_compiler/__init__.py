import re
from markdown_compiler.util.line_functions import (
    compile_headers,
    compile_bold_stars,
    compile_bold_underscore,
    compile_italic_star,
    compile_italic_underscore,
    compile_strikethrough,
    compile_code_inline,
    compile_images,
    compile_links,
)


def minify(html):
    '''
    Minifies HTML by stripping trailing/leading whitespace and collapsing spaces.
    '''
    return re.sub(r'\s+', ' ', html).strip()


def _compile_line(line):
    line = compile_headers(line)
    line = compile_bold_stars(line)
    line = compile_bold_underscore(line)
    line = compile_italic_star(line)
    line = compile_italic_underscore(line)
    line = compile_strikethrough(line)
    line = compile_code_inline(line)
    line = compile_images(line)
    line = compile_links(line)
    return line


def compile_lines(lines, add_css=False):
    '''
    Convert markdown lines to HTML paragraphs and code blocks.
    '''
    if isinstance(lines, str):
        lines = lines.splitlines(keepends=True)

    result = []

    if add_css:
        result.append('<link rel="stylesheet" href="style.css">\n')
        result.append('<link rel="stylesheet" href="custom.css">\n')

    in_p = False
    in_code = False

    for idx, line in enumerate(lines):
        stripped = line.strip()

        if idx == 0 and not stripped:
            result.append('\n')
            continue

        if stripped.startswith('```'):
            if not in_code:
                if in_p:
                    result.append('</p>\n')
                    in_p = False
                in_code = True
                result.append('<pre>\n')
            else:
                in_code = False
                result.append('</pre>\n')
            continue

        if in_code:
            result.append(line)
            continue

        if not stripped:
            if in_p:
                result.append('</p>\n')
                in_p = False
            if idx == len(lines) - 1:
                result.append('\n')
            continue

        compiled = _compile_line(line)
        if compiled.startswith('<h'):
            if in_p:
                result.append('</p>\n')
                in_p = False
            result.append(compiled)
            continue

        if not in_p:
            in_p = True
            result.append('<p>\n')

        result.append(compiled)

    if in_p:
        result.append('</p>')

    return ''.join(result)


def markdown_to_html(markdown_text, add_css=False):
    '''
    Converts markdown text to a full HTML document.
    '''
    compiled_body = compile_lines(markdown_text, add_css=add_css)
    return (
        "<!DOCTYPE html>\n"
        "<html>\n"
        "<head>\n"
        '  <meta charset="utf-8">\n'
        "  <title>Compiled Markdown</title>\n"
        "</head>\n"
        "<body>\n"
        f"{compiled_body}\n"
        "</body>\n"
        "</html>"
    )
