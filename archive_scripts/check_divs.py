from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []
        self.errors = []

    def handle_starttag(self, tag, attrs):
        if tag in ['div', 'section']:
            self.stack.append((tag, self.getpos()))

    def handle_endtag(self, tag):
        if tag in ['div', 'section']:
            if not self.stack:
                self.errors.append(f"Extra closing tag </{tag}> at line {self.getpos()[0]}")
            else:
                last_tag, pos = self.stack.pop()
                if last_tag != tag:
                    self.errors.append(f"Mismatched closing tag. Expected </{last_tag}> (opened at line {pos[0]}), got </{tag}> at line {self.getpos()[0]}")

parser = MyHTMLParser()
with open('index.html', 'r', encoding='utf-8') as f:
    parser.feed(f.read())

for err in parser.errors:
    print(err)
if parser.stack:
    print(f"Unclosed tags at end: {parser.stack}")
