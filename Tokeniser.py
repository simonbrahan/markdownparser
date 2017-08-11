from itertools import takewhile

def get_tokens(markdown):
    token = get_next_token(markdown)
    if not token:
        return []
    else:
        return [token] + get_tokens(markdown[len(token):])


def get_next_token(markdown):
    if len(markdown) is 0:
        return False

    if is_special_char(markdown[0]):
        return markdown[0]

    is_text_char = lambda char: not is_special_char(char)

    return ''.join(takewhile(is_text_char, markdown))


def is_special_char(char):
    return char in ['_', '*', '\n']
