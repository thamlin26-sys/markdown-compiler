import re


def compile_headers(line):
    '''
    Compiles markdown headers (# Heading) to HTML tags (<h1>Heading</h1>\n).
    '''
    match = re.match(r'^(#{1,6})\s*(.*?)\n?$', line)
    if match:
        level = len(match.group(1))
        content = match.group(2).strip()
        return f'<h{level}>{content}</h{level}>\n'
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
    return re.sub(r'~~(.*?)~~', r'<del>\1</del>', line)


def compile_code_inline(line):
    return re.sub(r'`(.*?)`', r'<code>\1</code>', line)


def compile_links(line):
    return re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', line)


def compile_images(line):
    return re.sub(r'!\[(.*?)\]\((.*?)\)', r'<img src="\2" alt="\1" />', line)
