from langchain_core.messages import HumanMessage
from config.llm import llm

SUPERVISOR_PROMPT = """
You are a routing agent for Green IQ.

Classify the user query into ONLY ONE category:

1. doctor → plant disease, plant health, watering, pests, yellow leaves, etc.
2. search → plant name lookup, plant information, species details.

Rules:
- Return ONLY one word.
- No explanation.
- No punctuation.
- Only: doctor OR search
"""


def supervisor_agent(state):
    message = state["message"]

    response = llm.invoke([
        HumanMessage(
            content=f"""
{SUPERVISOR_PROMPT}

User message:
{message}
"""
        )
    ])

    intent = response.content.strip().lower()

    if intent not in ["doctor", "search"]:
        intent = "doctor" 

    state["intent"] = intent
    return state