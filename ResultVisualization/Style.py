def has_color(style: str) -> bool:
    return style and style[0] in {'b', 'g', 'r', 'c', 'm', 'y', 'k', 'w'}


def validate(style: str) -> bool:
    if not style:
        return False

    if has_color(style):
        style = style[1:]

    markers = {
        '.', ',', 'o', 'v',
        '^', '<', '>', '1',
        '2', '3', '4', 's',
        'p', '*', 'h', 'H',
        '+', 'x', 'D', 'd',
        '|', '_'
    }

    for marker in markers:
        if style[0:len(marker)] == marker:
            style = style[len(marker):]
            break

    lineStyles = [
        '--', '-.', '-', ':'
    ]

    for lineStyle in lineStyles:
        tmp = style[0:len(lineStyle)]

        if tmp == lineStyle:
            style = style[len(lineStyle):]
            break

    return not style
