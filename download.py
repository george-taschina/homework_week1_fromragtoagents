"""Download all PDFs listed in books.csv."""
import csv
import os
import urllib.request

os.makedirs("books", exist_ok=True)

with open("books.csv") as f:
    rows = list(csv.DictReader(f))

for row in rows:
    title = row["title"]
    url = row["pdf_url"]
    name = os.path.basename(url.split("?")[0])
    dest = os.path.join("books", name)
    if os.path.exists(dest) and os.path.getsize(dest) > 0:
        print(f"skip {title}: {dest}")
        continue
    print(f"downloading {title} <- {url}")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as r, open(dest, "wb") as out:
        out.write(r.read())
    print(f"  saved {dest} ({os.path.getsize(dest)} bytes)")
