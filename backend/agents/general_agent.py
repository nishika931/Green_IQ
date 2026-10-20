
from langchain_core.messages import HumanMessage
from config.llm import llm


SYSTEM_PROMPT = """
You are Green IQ's General Assistant, a plant-care and
gardening assistant.

Answer questions about plants, gardening, plant biology,
soil, watering, and plant health.

Use the provided Green IQ knowledge when relevant.
If it is insufficient, use general knowledge for
plant-related questions when you can answer reliably.

Use conversation memory to understand follow-up questions.
Do not invent facts or unsupported treatment details.

For completely unrelated questions, briefly respond:
"I'm Green IQ, a plant-care and gardening assistant.
I can help with plants, gardening, soil, watering,
and plant health."

Do not mention internal processing.
Keep answers simple and beginner-friendly.
"""


def general_agent(state):

    message = state["message"].strip()
    normalized = message.lower().strip(" .!?,")

    greetings = {
        "hi", "hello", "hey",
        "hi there", "hello there",
        "good morning", "good afternoon", "good evening"
    }

    if normalized in greetings:
        state["response"] = (
            "Hi! 🌱 I'm Green IQ, your plant-care assistant. "
            "How can I help you with your plants today?"
        )
        return state

    context = state.get("context", "")
    memory = state.get("memory", "")

    prompt = f"""
{SYSTEM_PROMPT}

Recent conversation:
{memory}

Relevant Green IQ plant-care knowledge:
{context}

Current user question:
{message}

Answer clearly and naturally.
"""

    response = llm.invoke(
        [HumanMessage(content=prompt)]
    )

    state["response"] = response.content
    return state
