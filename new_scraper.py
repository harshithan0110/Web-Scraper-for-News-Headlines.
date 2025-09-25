import requests
from bs4 import BeautifulSoup

URL = "https://timesofindia.indiatimes.com/"

resp = requests.get(URL, timeout=10)
resp.raise_for_status()   # will raise an error if request failed

soup = BeautifulSoup(resp.text, "html.parser")

headlines = []
seen = set()

# Try common headline containers: h2, h3, and anchor tags that look like headlines
for tag in soup.find_all(["h1", "h2", "h3", "a"]):
    text = tag.get_text(strip=True)
    if not text:
        continue

    # simple heuristic: skip very short words like "Read" or "More"
    if len(text) < 10:
        continue

    # filter out obvious nav/footer repeats by ignoring if too long or contains "\n"
    text = " ".join(text.split())

    if text not in seen:
        seen.add(text)
        headlines.append(text)

# Print top 25 (or fewer) headlines
for i, h in enumerate(headlines[:25], 1):
    print(f"{i}. {h}")

# Save to file
with open("toi_headlines.txt", "w", encoding="utf-8") as f:
    for h in headlines:
        f.write(h + "\n")

print(f"\n✅ Saved {len(headlines)} headlines to toi_headlines.txt")