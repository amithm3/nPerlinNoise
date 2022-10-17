# readme.py

def findOpenClose(string, char: tuple[str, str]):
    i = _i = string.find(char[0])
    ie = string.find(char[1])
    while string.count(char[0], i + 1, ie) != string.count(char[1], i + 1, ie):
        ie = string.find(char[1], ie + 1)
    return i, ie


def embed_link(link):
    ignore = ["#usage"]
    raw = ['.png', '.txt']
    branch = 'v0.1.3-alpha_dev'
    base_raw = f'https://raw.github.com/Amith225/nPerlinNoise/{branch}/'
    base = f'https://github.com/Amith225/nPerlinNoise/blob/{branch}/'
    if not link.startswith('http') and link not in ignore:
        link = (base_raw if any(link.endswith(r) for r in raw) else base) + link
    return link


def embed(content: str):
    i, ie = findOpenClose(content, ('[', ']'))
    if i == -1 or ie == -1: return content
    if content[ie + 1] == '(':
        alt_txt = content[i + 1:ie]
        li, lie = findOpenClose(content[ie + 1:], ('(', ')'))
        link = content[li + ie + 2:lie + ie + 1]
        ie = lie + ie + 1
        _embed_ = f"[{embed(alt_txt)}]({embed_link(link)})"
        print(_embed_)
    else:
        _embed_ = content[i:ie + 1]
    return content[:i] + _embed_ + embed(content[ie + 1:])


if __name__ == '__main__':
    with open('docs/README_EMBED.md', 'w+') as wFile:
        with open('README.md', 'r') as rFile:
            wFile.write(embed(rFile.read()))
