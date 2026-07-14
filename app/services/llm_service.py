import os

from dotenv import load_dotenv
from groq import Groq


load_dotenv()


MODEL_NAME = "llama-3.3-70b-versatile"

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def generate_answer(
    query: str,
    context_chunks: list[str],
    history: list[dict] | None = None,
) -> str:
    context = "\n\n---\n\n".join(context_chunks)

    system_prompt = """
You are an AI research assistant.

Answer the user's question using only the provided context.

Rules:
- Do not use outside knowledge.
- Do not invent facts.
- If the answer is not present in the context, say:
  "I could not find this information in the uploaded document."
- Give a clear and concise answer.
"""

    user_prompt = f"""
CONTEXT:

{context}

QUESTION:

{query}
"""

    messages = [
        {
            "role": "system",
            "content": system_prompt,
        }
    ]

    if history:
        messages.extend(history)

    messages.append(
        {
            "role": "user",
            "content": user_prompt,
        }
    )

    completion = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        temperature=0.2,
    )

    return completion.choices[0].message.content