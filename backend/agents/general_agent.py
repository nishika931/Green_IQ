from langchain_core.messages import HumanMessage

from config.llm import llm


SYSTEM_PROMPT = """
You are Green IQ.

You are a smart AI Plant Care Assistant.

You can:

- Answer plant-related questions.
- Give gardening tips.
- Help beginners.
- Have friendly conversations.

If a question requires weather or plant database information,
the Supervisor Agent will route it elsewhere.

Be concise and helpful.
"""


def general_agent(state):

    message = state["message"]

    response = llm.invoke([
        HumanMessage(
            content=f"""
{SYSTEM_PROMPT}

User:
{message}
"""
        )
    ])

    state["response"] = response.content

    return state