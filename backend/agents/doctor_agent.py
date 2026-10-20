
from langchain_core.messages import HumanMessage

from config.llm import llm
from tools.weather_tool import weather_tool


def doctor_agent(state):

    message = state["message"]
    context = state.get("context", "")
    memory = state.get("memory", "")
    city = state.get("city")
    plant_name = state.get("plant_name")

    weather_data = None

    if city:
        try:
            weather_data = weather_tool.invoke(city)
        except Exception as e:
            print(f"Weather tool error: {e}")

    prompt = f"""
You are Green IQ Plant Doctor, a beginner-friendly
plant-care assistant.

USER QUESTION:
{message}

PLANT NAME:
{plant_name or "Not identified"}

PLANT-CARE KNOWLEDGE:
{context}

RECENT CONVERSATION:
{memory}

WEATHER DATA:
{weather_data}


INSTRUCTIONS:
1. Answer only the user's exact question. Do not provide a complete
   plant-care guide unless the user asks for one.
2. Use the provided plant-care knowledge as the primary source.
3. If the user asks for a specific fact, check whether that fact
   appears in the provided knowledge.
4. If the fact is present, answer using that information.
5. If the fact is missing, clearly say that the provided knowledge
   does not specify it. You may add reliable general knowledge,
   but clearly label it as general guidance rather than information
   from the provided knowledge.
6. Never claim a fact came from the knowledge base if it isn't there.
7. Use weather data only when relevant to the question.
8. Use conversation memory to understand references, not as
   verified plant-care evidence.
9. Keep the answer simple, concise, and beginner-friendly.
10. Do not include information about unrelated plants.
11. Do not mention RAG, databases, APIs, or internal processing.
"""

    response = llm.invoke(
        [HumanMessage(content=prompt)]
    )

    state["weather"] = weather_data
    state["response"] = response.content

    return state
