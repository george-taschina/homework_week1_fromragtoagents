"""Homework Q3-Q4: build the minsearch index and run the search."""
import json

from minsearch import Index

QUERY = "python function definition"


def prepare_documents(chunks):
    documents = []
    for chunk in chunks:
        doc = dict(chunk)
        doc["content"] = "\n".join(chunk["content"])
        documents.append(doc)
    return documents


def main():
    with open("chunks.json") as f:
        chunks = json.load(f)

    documents = prepare_documents(chunks)
    print(f"documents to index: {len(documents)}")

    index = Index(text_fields=["content"])
    index.fit(documents)
    print("index fitted")

    results = index.search(QUERY, num_results=5)
    print(f"\n=== Q4: search {QUERY!r} ===")
    for i, r in enumerate(results, 1):
        print(f"{i}. {r['source']}  (start={r.get('start')})")
        print("   " + r["content"][:200].replace("\n", "\n   "))
    print("\nTOP RESULT SOURCE:", results[0]["source"])

    with open("search_results.json", "w") as f:
        json.dump(results, f, indent=2)


if __name__ == "__main__":
    main()
