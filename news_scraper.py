from urllib.request import Request, urlopen
from html.parser import HTMLParser

class HParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.capture = False
        self.buf = []
        self.headlines = []

    def handle_starttag(self, tag, attrs):
        if tag in ("h2", "h3"):
            self.capture = True
            self.buf = []

    def handle_endtag(self, tag):
        if tag in ("h2", "h3") and self.capture:
            text = " ".join(self.buf).strip()
            if text and len(text) > 5:
                self.headlines.append(text)
            self.capture = False
            self.buf = []

    def handle_data(self, data):
        if self.capture:
            self.buf.append(data.strip())

req = Request("https://www.deccanherald.com/", headers={"User-Agent": "Mozilla/5.0"})
html = urlopen(req, timeout=15).read().decode("utf-8", errors="replace")
p = HParser()
p.feed(html)

with open("deccanherald_headlines_no_bs4.txt", "w", encoding="utf-8") as f:
    for i, h in enumerate(p.headlines, 1):
        f.write(f"{i}. {h}\n")
print("Saved", len(p.headlines), "headlines to deccanherald_headlines_no_bs4.txt")
