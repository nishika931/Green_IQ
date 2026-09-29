from ai.rag import retrieve_context
from ai.memory import add_message, get_memory_text
from config.llm import llm


def ask_with_rag(question: str, user_id: int = 1):

    memory_text = get_memory_text(
        user_id,
        limit=4
    )

    context = retrieve_context(
        question,
        k=2
    )

    prompt = f"""
You are Green IQ, an AI plant-care assistant.

Your job is to answer the user's question using ONLY the
provided plant-care knowledge and relevant conversation memory.

STRICT RULES:
1. Do not add facts that are not supported by the provided knowledge.
2. Do not invent treatments, measurements, fertilizer schedules,
   dosages, or environmental requirements.
3. If the provided knowledge does not contain enough information,
   clearly say:
   "I don't have enough information in my current plant-care knowledge."
4. Keep the answer concise and practical.
5. Use conversation memory only to understand references such as
   "it", "this plant", or "that problem".
6. Do not treat the conversation memory as factual plant-care
   knowledge unless the same information is supported by the
   provided knowledge.

Recent conversation:
{memory_text}

Provided plant-care knowledge:
{context}

Current user question:
{question}
"""

    response = llm.invoke(prompt)

    answer = response.content

    add_message(
        user_id,
        "user",
        question
    )

    add_message(
        user_id,
        "assistant",
        answer
    )

    return answer