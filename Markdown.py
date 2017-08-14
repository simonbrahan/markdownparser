import Tokeniser, Parser

def to_html(markdown):
    tokens = Tokeniser.get_tokens(' **bold text** *italic text*')
    return Parser.match_all_sentences(tokens)
