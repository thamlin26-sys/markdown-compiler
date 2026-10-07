'''
Each of the functions in this file takes a single line of input and transforms the line in some way.
'''


def compile_headers(line):
    '''
    Convert markdown headers into <h1>,<h2>,etc tags.

    >>> compile_headers('# This is the main header')
    '<h1> This is the main header</h1>'
    >>> compile_headers('## This is a sub-header')
    '<h2> This is a sub-header</h2>'
    >>> compile_headers('### This is a sub-header')
    '<h3> This is a sub-header</h3>'
    >>> compile_headers('#### This is a sub-header')
    '<h4> This is a sub-header</h4>'
    >>> compile_headers('##### This is a sub-header')
    '<h5> This is a sub-header</h5>'
    >>> compile_headers('###### This is a sub-header')
    '<h6> This is a sub-header</h6>'
    >>> compile_headers('      # this is not a header')
    '      # this is not a header'
    '''
    if line.startswith('######'):
        return '<h6>' + line[6:] + '</h6>'
    elif line.startswith('#####'):
        return '<h5>' + line[5:] + '</h5>'
    elif line.startswith('####'):
        return '<h4>' + line[4:] + '</h4>'
    elif line.startswith('###'):
        return '<h3>' + line[3:] + '</h3>'
    elif line.startswith('##'):
        return '<h2>' + line[2:] + '</h2>'
    elif line.startswith('#'):
        return '<h1>' + line[1:] + '</h1>'
    return line


def _compile_delimiter(line, delimiter, open_tag, close_tag):
    '''Helper function to transform symmetric delimiters into HTML tags.'''
    start = 0
    while True:
        first = line.find(delimiter, start)
        if first == -1:
            break
        second = line.find(delimiter, first + len(delimiter))
        if second == -1:
            break

        inside = line[first + len(delimiter):second]
        replacement = open_tag + inside + close_tag
        line = line[:first] + replacement + line[second + len(delimiter):]
        start = first + len(replacement)

    return line


def compile_italic_star(line):
    '''
    Convert "*italic*" into "<i>italic</i>".

    >>> compile_italic_star('*This is italic!* This is not italic.')
    '<i>This is italic!</i> This is not italic.'
    >>> compile_italic_star('*This is italic!*')
    '<i>This is italic!</i>'
    >>> compile_italic_star('This is *italic*!')
    'This is <i>italic</i>!'
    >>> compile_italic_star('This is not *italic!')
    'This is not *italic!'
    >>> compile_italic_star('*')
    '*'
    '''
    return _compile_delimiter(line, '*', '<i>', '</i>')


def compile_italic_underscore(line):
    '''
    Convert "_italic_" into "<i>italic</i>".


    >>> compile_italic_underscore('_This is italic!_ This is not italic.')
    '<i>This is italic!</i> This is not italic.'
    >>> compile_italic_underscore('_This is italic!_')
    '<i>This is italic!</i>'
    >>> compile_italic_underscore('This is _italic_!')
    'This is <i>italic</i>!'
    >>> compile_italic_underscore('This is not _italic!')
    'This is not _italic!'
    >>> compile_italic_underscore('_')
    '_'
    '''
    return _compile_delimiter(line, '_', '<i>', '</i>')


def compile_strikethrough(line):
    '''
    Convert "~~strikethrough~~" to "<ins>strikethrough</ins>".

    >>> compile_strikethrough('~~This is strikethrough!~~ This is not strikethrough.')
    '<ins>This is strikethrough!</ins> This is not strikethrough.'
    >>> compile_strikethrough('~~This is strikethrough!~~')
    '<ins>This is strikethrough!</ins>'
    >>> compile_strikethrough('This is ~~strikethrough~~!')
    'This is <ins>strikethrough</ins>!'
    >>> compile_strikethrough('This is not ~~strikethrough!')
    'This is not ~~strikethrough!'
    >>> compile_strikethrough('~~')
    '~~'
    '''
    return _compile_delimiter(line, '~~', '<ins>', '</ins>')


def compile_bold_stars(line):
    '''
    Convert "**bold**" to "<b>bold</b>".

    >>> compile_bold_stars('**This is bold!** This is not bold.')
    '<b>This is bold!</b> This is not bold.'
    >>> compile_bold_stars('**This is bold!**')
    '<b>This is bold!</b>'
    >>> compile_bold_stars('This is **bold**!')
    'This is <b>bold</b>!'
    >>> compile_bold_stars('This is not **bold!')
    'This is not **bold!'
    >>> compile_bold_stars('**')
    '**'
    '''
    return _compile_delimiter(line, '**', '<b>', '</b>')


def compile_bold_underscore(line):
    '''
    Convert "__bold__" to "<b>bold</b>".

    >>> compile_bold_underscore('__This is bold!__ This is not bold.')
    '<b>This is bold!</b> This is not bold.'
    >>> compile_bold_underscore('__This is bold!__')
    '<b>This is bold!</b>'
    >>> compile_bold_underscore('This is __bold__!')
    'This is <b>bold</b>!'
    >>> compile_bold_underscore('This is not __bold!')
    'This is not __bold!'
    >>> compile_bold_underscore('__')
    '__'
    '''
    return _compile_delimiter(line, '__', '<b>', '</b>')


def compile_code_inline(line):
    '''
    Add <code> tags.

    >>> compile_code_inline('You can use backticks like this (`1+2`) to include code in the middle of text.')
    'You can use backticks like this (<code>1+2</code>) to include code in the middle of text.'
    >>> compile_code_inline('This is inline code: `1+2`')
    'This is inline code: <code>1+2</code>'
    >>> compile_code_inline('`1+2`')
    '<code>1+2</code>'
    >>> compile_code_inline('This example has html within the code: `<b>bold!</b>`')
    'This example has html within the code: <code>&lt;b&gt;bold!&lt;/b&gt;</code>'
    >>> compile_code_inline('this example has a math formula in the  code: `1 + 2 < 4`')
    'this example has a math formula in the  code: <code>1 + 2 &lt; 4</code>'
    >>> compile_code_inline('this example has a <b>math formula</b> in the  code: `1 + 2 < 4`')
    'this example has a <b>math formula</b> in the  code: <code>1 + 2 &lt; 4</code>'
    >>> compile_code_inline('```')
    '```'
    >>> compile_code_inline('```python3')
    '```python3'
    '''
    # Ignore fenced code block lines starting with ```
    if line.startswith('```'):
        return line

    start = 0
    while True:
        first = line.find('`', start)
        if first == -1:
            break
        second = line.find('`', first + 1)
        if second == -1:
            break

        inside = line[first + 1:second]
        inside = inside.replace('<', '&lt;').replace('>', '&gt;')
        replacement = '<code>' + inside + '</code>'
        line = line[:first] + replacement + line[second + 1:]
        start = first + len(replacement)

    return line


def compile_links(line):
    '''
    Add <a> tags.

    >>> compile_links('Click on the [course webpage](https://github.com/mikeizbicki/cmc-csci040)!')
    'Click on the <a href="https://github.com/mikeizbicki/cmc-csci040">course webpage</a>!'
    >>> compile_links('[course webpage](https://github.com/mikeizbicki/cmc-csci040)')
    '<a href="https://github.com/mikeizbicki/cmc-csci040">course webpage</a>'
    >>> compile_links('this is wrong: [course webpage]    (https://github.com/mikeizbicki/cmc-csci040)')
    'this is wrong: [course webpage]    (https://github.com/mikeizbicki/cmc-csci040)'
    >>> compile_links('this is wrong: [course webpage](https://github.com/mikeizbicki/cmc-csci040')
    'this is wrong: [course webpage](https://github.com/mikeizbicki/cmc-csci040'
    '''
    start = 0
    while True:
        bracket_open = line.find('[', start)
        if bracket_open == -1:
            break
        # Ignore images (which start with '!')
        if bracket_open > 0 and line[bracket_open - 1] == '!':
            start = bracket_open + 1
            continue

        bracket_close = line.find(']', bracket_open)
        if bracket_close == -1:
            break

        if bracket_close + 1 < len(line) and line[bracket_close + 1] == '(':
            paren_open = bracket_close + 1
            paren_close = line.find(')', paren_open)
            if paren_close == -1:
                break

            text = line[bracket_open + 1:bracket_close]
            url = line[paren_open + 1:paren_close]
            replacement = f'<a href="{url}">{text}</a>'
            line = line[:bracket_open] + replacement + line[paren_close + 1:]
            start = bracket_open + len(replacement)
        else:
            start = bracket_close + 1

    return line


def compile_images(line):
    '''
    Add <img> tags.

    >>> compile_images('[Mike Izbicki](https://avatars1.githubusercontent.com/u/1052630?v=2&s=460)')
    '[Mike Izbicki](https://avatars1.githubusercontent.com/u/1052630?v=2&s=460)'
    >>> compile_images('![Mike Izbicki](https://avatars1.githubusercontent.com/u/1052630?v=2&s=460)')
    '<img src="https://avatars1.githubusercontent.com/u/1052630?v=2&s=460" alt="Mike Izbicki" />'
    >>> compile_images('This is an image of Mike Izbicki: ![Mike Izbicki](https://avatars1.githubusercontent.com/u/1052630?v=2&s=460)')
    'This is an image of Mike Izbicki: <img src="https://avatars1.githubusercontent.com/u/1052630?v=2&s=460" alt="Mike Izbicki" />'
    '''
    start = 0
    while True:
        excl_open = line.find('![', start)
        if excl_open == -1:
            break

        bracket_close = line.find(']', excl_open)
        if bracket_close == -1:
            break

        if bracket_close + 1 < len(line) and line[bracket_close + 1] == '(':
            paren_open = bracket_close + 1
            paren_close = line.find(')', paren_open)
            if paren_close == -1:
                break

            alt_text = line[excl_open + 2:bracket_close]
            url = line[paren_open + 1:paren_close]
            replacement = f'<img src="{url}" alt="{alt_text}" />'
            line = line[:excl_open] + replacement + line[paren_close + 1:]
            start = excl_open + len(replacement)
        else:
            start = bracket_close + 1

    return line
