"""Homework: Document Processing with AI - steps for Q1-Q4."""
import json
import os

from gitsource import chunk_documents

BOOKS_TEXT_DIR = "books_text"
THINK_PYTHON = "thinkpython2.md"


def prepare_raw_documents():
    """Read each markdown file, split into lines, drop empty/whitespace-only lines."""
    documents = []
    for name in sorted(os.listdir(BOOKS_TEXT_DIR)):
        if not name.endswith(".md"):
            continue
        with open(os.path.join(BOOKS_TEXT_DIR, name)) as f:
            lines = f.read().split("\n")
        lines = [line for line in lines if line.strip()]
        documents.append({"source": name, "content": lines})
    return documents


def main():
    documents = prepare_raw_documents()

    print("=== Q1: lines in Think Python 2e ===")
    tp = [d for d in documents if d["source"] == THINK_PYTHON][0]
    print(f"non-empty lines: {len(tp['content'])}")

    print("\n=== Q2: chunks for Think Python 2e (size=100, step=50) ===")
    tp_chunks = chunk_documents([tp], size=100, step=50)
    print(f"chunks: {len(tp_chunks)}")
    print(f"first chunk content lines: {len(tp_chunks[0]['content'])}")

    print("\n=== Q3: index all chunks ===")
    all_chunks = chunk_documents(documents, size=100, step=50)
    print(f"total chunks: {len(all_chunks)}")
    per_book = {}
    for c in all_chunks:
        per_book[c["source"]] = per_book.get(c["source"], 0) + 1
    for k, v in sorted(per_book.items()):
        print(f"  {k}: {v}")

    # save for later steps
    with open("chunks.json", "w") as f:
        json.dump(all_chunks, f)
    print("\nsaved chunks.json")


if __name__ == "__main__":
    main()
