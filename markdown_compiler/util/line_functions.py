import re


def compile_headers(line):
    '''
    Compiles markdown headers (# Heading) to HTML tags (<h1> Heading</h1>).
    '''
    match = re.match(r'^(#{1,6})(.*)$', line)
    if match:
        level = len(match.group(1))
        content = match.group(2)
        return f'<h{level}>{content}</h{level}>'
    return line


def compile_bold_stars(line):
    return re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line)


def compile_bold_underscore(line):
    return re.sub(r'__(.*?)__', r'<b>\1</b>', line)


def compile_italic_star(line):
    return re.sub(r'(?<!\*)\*(?!\*)(.*?)(?<!\*)\*(?!\*)', r'<i>\1</i>', line)


def compile_italic_underscore(line):
    return re.sub(r'(?<!_)_(?!_)(.*?)(?<!_)_(?!_)', r'<i>\1</i>', line)


def compile_strikethrough(line):
    return re.sub(r'~~(.*?)~~', r'<ins>\1</ins>', line)


def compile_code_inline(line):
    return re.sub(r'`(.*?)`', r'<code>\1</code>', line)


def compile_images(line):
    return re.sub(r'!\[(.*?)\]\((.*?)\)', r'<img src="\2" alt="\1" />', line)


def compile_links(line):
    return re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', line)
