from itertools import takewhile

class Token():
    def __init__(self, token_type, value):
        self.token_type = token_type
        self.value = value

    def __repr__(self):
        return str(self.__dict__)


def get_tokens(markdown):
    token = get_next_token(markdown)
    if not token:
        return []
    else:
        return [token] + get_tokens(markdown[len(token.value):])


def get_next_token(markdown):
    if len(markdown) is 0:
        return False

    special_char_type = get_special_char_type(markdown[0])
    if special_char_type is not None:
        return Token(special_char_type, markdown[0])

    is_text_char = lambda char: get_special_char_type(char) is None

    return Token(
        'TEXT',
        ''.join(takewhile(is_text_char, markdown))
    )


def get_special_char_type(char):
    char_types = {
        '_': 'UNDERSCORE',
        '*': 'STAR',
        '\n': 'NEWLINE'
    }

    if char in char_types.keys():
        return char_types[char]
    else:
        return None
