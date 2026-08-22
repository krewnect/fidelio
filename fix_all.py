from html.parser import HTMLParser

class BalanceParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.div_depth = 0
        self.in_builder = False
        self.builder_start_depth = 0
    def handle_starttag(self, tag, attrs):
        if tag == 'section' and ('id', 'tab-builder') in attrs:
            self.in_builder = True
            self.builder_start_depth = self.div_depth
        if tag == 'div':
            self.div_depth += 1
    def handle_endtag(self, tag):
        if tag == 'div':
            self.div_depth -= 1
        if tag == 'section' and self.in_builder:
            print(f"End of tab-builder. Div depth diff: {self.div_depth - self.builder_start_depth}")
            self.in_builder = False

p = BalanceParser()
with open('index.html', 'r', encoding='utf-8') as f:
    p.feed(f.read())
print("Final depth:", p.div_depth)
