class Node():
    def __init__(self, node_type, value, consumed):
        self.type = node_type
        self.value = value
        self.consumed = consumed

    def __repr__(self):
        return str(self.__dict__)

def match_paragraph(tokens):
    return match_all_sentences(tokens)


def match_all_sentences(tokens):
    sentence = match_sentence(tokens)
    if sentence:
        return [sentence] + match_all_sentences(tokens[sentence.consumed:])
    else:
        return []


def match_sentence(tokens):
    return match_first(tokens, match_bold_text, match_italic_text, match_text)


def match_text(tokens):
    if len(tokens) is 0:
        return False

    if tokens[0].type == 'TEXT':
        return Node('TEXT', tokens[0].value, 1)
    else:
        return False


def match_bold_text(tokens):
    if match_any_set(
        tokens,
        (
            ('STAR', 'STAR', 'TEXT', 'STAR', 'STAR'),
            ('UNDERSCORE', 'UNDERSCORE', 'TEXT', 'UNDERSCORE', 'UNDERSCORE')
        )
    ):
        return Node('BOLD', tokens[2].value, 5)
    else:
        return False


def match_italic_text(tokens):
    if match_any_set(
        tokens,
        (
            ('STAR', 'TEXT', 'STAR'),
            ('UNDERSCORE', 'TEXT', 'UNDERSCORE')
        )
    ):
        return Node('ITALIC', tokens[1].value, 3)
    else:
        return False


def match_any_set(tokens, match_sets):
    if len(tokens) is 0:
        return False

    for match_set in match_sets:
        if match_single_set(tokens, match_set):
            return True

    return False


def match_single_set(tokens, match_set):
    for token_idx, match_item in enumerate(match_set):
        try:
            if tokens[token_idx].type != match_item:
                return False
        except IndexError:
            return False

    return True

def match_first(tokens, *matchers):
    for matcher in matchers:
        node = matcher(tokens)
        if node:
            return node

    return False
