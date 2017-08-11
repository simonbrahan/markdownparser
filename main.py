import Markdown

with open('text.md') as source:
    print Markdown.to_html(source.read())
