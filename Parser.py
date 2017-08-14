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


def match_text_tokens(tokens):
    if len(tokens) is 0:
        return False

    token_idx = 0
    text_tokens = []

    def is_text(tokens, token_idx):
        return tokens[token_idx].type == 'TEXT'

    def is_single_linebreak(tokens, token_idx):
        return tokens[token_idx].type == 'NEWLINE' and tokens[token_idx+1].type != 'NEWLINE'

    while token_idx < len(tokens):
        if is_text(tokens, token_idx):
            text_tokens.append(tokens[token_idx])
        elif is_single_linebreak(tokens, token_idx):
            text_tokens.append(tokens[token_idx])
        else:
            break

        token_idx += 1

    return text_tokens


def match_text(tokens):
    text_tokens = match_text_tokens(tokens)

    if len(text_tokens) > 0:
        return Node(
            'TEXT',
            ''.join([token.value for token in text_tokens]),
            len(text_tokens)
        )
    else:
        return False


def match_bold_text(tokens):
    def match_double_star(tokens):
        return (
            len(tokens) > 1 and
            tokens[0].type == 'STAR' and
            tokens[1].type == 'STAR'
        )

    def match_double_underscore(tokens):
        return (
            len(tokens) > 1 and
            tokens[0].type == 'UNDERSCORE'
            and tokens[1].type == 'UNDERSCORE'
        )

    starts_double_star = match_double_star(tokens)
    starts_double_underscore = match_double_underscore(tokens)
    if not starts_double_star and not starts_double_underscore:
        return False

    text_tokens = match_text_tokens(tokens[2:])

    unfinished_double_star = (
        starts_double_star and not
        match_double_star(tokens[len(text_tokens) + 2:])
    )

    unfinished_double_underscore = (
        starts_double_underscore and not
        match_double_underscore(tokens[len(text_tokens) + 2:])
    )

    if unfinished_double_star or unfinished_double_underscore:
        raise Exception('mismatched bold tokens')

    return Node(
        'BOLD',
        ''.join([token.value for token in text_tokens]),
        len(text_tokens) + 4
    )


def match_italic_text(tokens):
    def match_single_star(tokens):
        return (
            len(tokens) >= 2 and
            tokens[0].type == 'STAR' and
            tokens[1].type != 'STAR'
        )

    def match_single_underscore(tokens):
        return (
            len(tokens) > 2 and
            tokens[0].type == 'UNDERSCORE'
            and tokens[1].type != 'UNDERSCORE'
        )

    starts_single_star = match_single_star(tokens)
    starts_single_underscore = match_single_underscore(tokens)
    if not starts_single_star and not starts_single_underscore:
        return False

    text_tokens = match_text_tokens(tokens[1:])

    unfinished_single_star = (
        starts_single_star and not
        match_single_star(tokens[len(text_tokens) + 1:])
    )

    unfinished_single_underscore = (
        starts_single_underscore and not
        match_single_underscore(tokens[len(text_tokens) + 1:])
    )

    if unfinished_single_star or unfinished_single_underscore:
        raise Exception('mismatched bold tokens')

    return Node(
        'BOLD',
        ''.join([token.value for token in text_tokens]),
        len(text_tokens) + 2
    )


def match_first(tokens, *matchers):
    for matcher in matchers:
        node = matcher(tokens)
        if node:
            return node

    return False
