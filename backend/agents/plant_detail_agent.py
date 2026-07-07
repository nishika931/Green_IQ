from langchain_core.messages import HumanMessage

from config.llm import llm
from tools.perenual_tool import plant_info_tool


SYSTEM_PROMPT = """
You are the Plant Detail Agent of Green IQ.

Your job is to provide accurate plant information using the tool.

Rules:
- Always use the plant_info_tool for plant data.
- If tool returns data, summarize it clearly.
- Include:
  - Common name
  - Scientific name
  - Watering
  - Sunlight
  - Care level
  - Description
- Be simple and user friendly.
"""


def plant_detail_agent(state):

    message = state["message"]

    plant_name = message

    plant_data = plant_info_tool.invoke(plant_name)

    state["plant_name"] = plant_name
    state["plant_data"] = plant_data

    response = llm.invoke([
        HumanMessage(
            content=f"""
{SYSTEM_PROMPT}

Plant Data:
{plant_data}

User Question:
{message}

Give a clean and helpful answer.
"""
        )
    ])

    state["response"] = response.content

    return state