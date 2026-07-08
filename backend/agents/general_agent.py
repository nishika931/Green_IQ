from langchain_core.messages import HumanMessage

from config.llm import llm


SYSTEM_PROMPT = """
You are Green IQ's General Assistant.

You are friendly, professional, and helpful.

Your responsibilities:
- Answer general plant-related questions.
- Give beginner gardening tips.
- Explain plant concepts in simple English.
- Have friendly conversations about plants.
- Help users learn about plant care.

"""


def general_agent(state):

    message = state["message"]

    response = llm.invoke([
        HumanMessage(
            content=f"""
{SYSTEM_PROMPT}

User Message:
{message}
"""
        )
    ])

    state["response"] = response.content

    return state