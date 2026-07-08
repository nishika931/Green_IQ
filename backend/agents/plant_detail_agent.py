from langchain_core.messages import HumanMessage

from config.llm import llm
from tools.perenual_tool import plant_info_tool


SYSTEM_PROMPT = """
You are Green IQ's Plant Detail Agent.

Your job is to answer questions using the plant information provided below.

Rules:
- Never mention tools, APIs, databases, or internal processing.
- Never say "I used the plant_info_tool" or "According to the tool".
- Write naturally, as if you already know the information.
- If the plant is not found, politely inform the user.
- Use the provided plant data to answer accurately.

Your response should include:
🌿 Common Name
🧬 Scientific Name
🌳 Family
📝 Description
☀ Sunlight
💧 Watering
⭐ Care Level

Keep the answer friendly and easy to read.
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