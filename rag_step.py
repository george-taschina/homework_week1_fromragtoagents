"""Homework Q5 + Q6: full RAG and the structured-output variant."""
import json
import os

from minsearch import Index
from openai import OpenAI
from pydantic import BaseModel, Field
from typing import Literal

QUERY = "python function definition"

instructions = """
You're a course assistant, your task is to answer the QUESTION from the
course students using the provided CONTEXT
"""
prompt_template = """
<QUESTION>
{question}
</QUESTION>
<CONTEXT>
{context}
</CONTEXT>
""".strip()


class RAGResponse(BaseModel):
    answer: str = Field(description="The main answer to the user's question in markdown")
    found_answer: bool = Field(description="True if relevant information was found in the documentation")
    confidence: float = Field(description="Confidence score from 0.0 to 1.0")
    confidence_explanation: str = Field(description="Explanation about the confidence level")
    answer_type: Literal["how-to", "explanation", "troubleshooting", "comparison", "reference"] = Field(
        description="The category of the answer"
    )
    followup_questions: list[str] = Field(description="Suggested follow-up questions")


def prepare_documents(chunks):
    documents = []
    for chunk in chunks:
        doc = dict(chunk)
        doc["content"] = "\n".join(chunk["content"])
        documents.append(doc)
    return documents


def build_prompt(question, search_results):
    context = json.dumps(search_results, indent=2)
    prompt = prompt_template.format(question=question, context=context).strip()
    return prompt


def main():
    with open("chunks.json") as f:
        chunks = json.load(f)
    documents = prepare_documents(chunks)
    index = Index(text_fields=["content"])
    index.fit(documents)

    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    def search(question):
        return index.search(question, num_results=5)

    # ---------- Q5: unstructured ----------
    search_results = search(QUERY)
    prompt = build_prompt(QUERY, search_results)
    messages = [
        {"role": "system", "content": instructions},
        {"role": "user", "content": prompt},
    ]
    response = client.responses.create(model="gpt-4o-mini", input=messages)
    print("=== Q5: unstructured RAG ===")
    print(f"prompt chars: {len(prompt)}")
    print(f"input tokens : {response.usage.input_tokens}")
    print(f"output tokens: {response.usage.output_tokens}")
    print("--- response ---")
    print(response.output_text)

    # ---------- Q6: structured ----------
    parsed = client.responses.parse(model="gpt-4o-mini", input=messages, text_format=RAGResponse)
    print("\n=== Q6: structured RAG ===")
    print(f"input tokens : {parsed.usage.input_tokens}")
    print(f"output tokens: {parsed.usage.output_tokens}")
    print("--- parsed ---")
    print(json.dumps(parsed.output_parsed.model_dump(), indent=2))

    diff = parsed.usage.input_tokens - response.usage.input_tokens
    print(f"\nMORE input tokens (structured - unstructured) = {diff}")


if __name__ == "__main__":
    main()
