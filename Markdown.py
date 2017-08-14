import Tokeniser, Parser

def to_html(markdown):
    with open('text.md') as source:
        tokens = Tokeniser.get_tokens(source.read())

    return Parser.match_body(tokens)
