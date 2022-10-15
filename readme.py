def find_all(a_str, sub, overlap=False):
    start_ = 0
    while True:
        start_ = a_str.find(sub, start_)
        if start_ == -1: return
        yield start_
        if overlap:
            start_ += 1
            continue
        start_ += len(sub)


def get_embed_readme():
    with open('README.md', 'r') as _file:
        content = _file.read()

    _content = ""
    _end = -1
    ignore = ["#usage"]
    raw = ['.png', '.txt']
    base_raw = 'https://raw.github.com/Amith225/NPerlinNoise/master/'
    base = 'https://github.com/Amith225/NPerlinNoise/blob/master/'
    for start, end in zip(find_all(content, '['), find_all(content, ']')):
        _content += content[_end + 1:start]
        end += 1
        alt_text = content[start:end]
        _start, _end = end + 1, content.find(')', end)
        link = content[_start:_end]
        if not link.startswith('http') and link not in ignore:
            link = (base_raw if any(link.endswith(r) for r in raw) else base) + link
        _content += alt_text + f"({link})"
    _content += content[_end + 1:]

    return _content


with open('README_pypi.md', 'w+') as file:
    file.write(get_embed_readme())
