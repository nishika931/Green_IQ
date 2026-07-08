from langchain_core.messages import HumanMessage
from config.llm import llm

SUPERVISOR_PROMPT = """
You are the Supervisor Agent of Green IQ.

Classify user query into ONLY ONE:

doctor
plant
weather
general


plant:
Use when user asks:
- tell me about a plant
- information about a plant
- care guide
- scientific name
- family
- sunlight
- watering requirements
- growth details
- characteristics


doctor:
Use when user asks:
- why are leaves yellow
- plant disease
- pests
- fungus
- brown leaves
- dying plant
- overwatering problem
- underwatering problem


weather:
Use when user asks:
- weather
- rain
- temperature
- humidity
- should I water today


general:
Use for:
- hello
- thanks
- casual conversation


IMPORTANT:
"Tell me about aloe vera", "What is snake plant", "Explain money plant"
MUST return:
plant


Return only one word:
doctor OR plant OR weather OR general
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

    if intent not in [
    "doctor",
    "plant",
    "weather",
    "general"
    ]:
        intent = "general"

    state["intent"] = intent
    return state