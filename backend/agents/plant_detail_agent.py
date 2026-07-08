from langchain_core.messages import HumanMessage

from config.llm import llm
from tools.perenual_tool import plant_info_tool


SYSTEM_PROMPT = """
You are the Plant Detail Agent of Green IQ.

Your job is to provide plant information using plant_info_tool.

Always:
- Extract the plant name from the user's message.
- Use plant_info_tool with only the plant name.
- Explain the result clearly.

Include:
- Common name
- Scientific name
- Family
- Watering
- Sunlight
- Soil
- Care level
- Description

Keep the answer simple and helpful.
"""


def plant_detail_agent(state):

    message = state["message"]

    # Extract plant name from user sentence
    extract_response = llm.invoke(
        f"""
Extract only the plant name from this sentence.

User:
{message}

Return only plant name.
"""
    )

    plant_name = extract_response.content.strip()

    # Call Perenual tool
    plant_data = plant_info_tool.invoke(plant_name)


    state["plant_name"] = plant_name
    state["plant_data"] = plant_data


    response = llm.invoke([
        HumanMessage(
            content=f"""
{SYSTEM_PROMPT}

Plant Name:
{plant_name}

Plant Data:
{plant_data}

User Question:
{message}

Give final answer.
"""
        )
    ])


    state["response"] = response.content

    return state