from langchain_core.messages import HumanMessage
from config.llm import llm

SUPERVISOR_PROMPT = """
You are the Supervisor Agent of Green IQ.

Your job is to decide which AI agent should answer.

Return ONLY ONE WORD.

doctor
plant
weather
general

Rules

doctor
- diseases
- pests
- yellow leaves
- brown leaves
- fungus
- overwatering
- underwatering

plant
- plant information
- scientific name
- family
- watering requirements
- sunlight
- care guide

weather
- weather
- rain
- temperature
- humidity
- watering today
- climate

general
- greetings
- thank you
- gardening tips
- casual plant conversation
- anything that doesn't require APIs
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