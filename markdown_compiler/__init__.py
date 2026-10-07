from markdown_compiler.util.line_functions import (
    compile_headers,
    compile_bold_stars,
    compile_bold_underscore,
    compile_italic_star,
    compile_italic_underscore,
    compile_strikethrough,
    compile_code_inline,
    compile_links,
    compile_images,
)


def _compile_line(line):
    line = compile_headers(line)
    line = compile_bold_stars(line)
    line = compile_bold_underscore(line)
    line = compile_italic_star(line)
    line = compile_italic_underscore(line)
    line = compile_strikethrough(line)
    line = compile_code_inline(line)
    line = compile_links(line)
    line = compile_images(line)
    return line


def compile_lines(lines, add_css=False):
    '''
    Convert markdown lines to HTML paragraphs and code blocks.
    '''
    if isinstance(lines, str):
        lines = lines.splitlines(keepends=True)

    result = []

    if add_css:
        css = "<style>\nbody { font-family: sans-serif; margin: 2rem; }\n</style>\n"
        result.append(css)

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
