"""Convert all PDFs in books/ to markdown in books_text/."""
import os

from markitdown import MarkItDown

os.makedirs("books_text", exist_ok=True)

md = MarkItDown()

for name in sorted(os.listdir("books")):
    if not name.lower().endswith(".pdf"):
        continue
    src = os.path.join("books", name)
    dst = os.path.join("books_text", os.path.splitext(name)[0] + ".md")
    if os.path.exists(dst):
        print(f"skip {dst}")
        continue
    print(f"converting {src} ...")
    result = md.convert(src)
    with open(dst, "w") as f:
        f.write(result.text_content)
    print(f"  -> {dst} ({os.path.getsize(dst)} bytes)")
