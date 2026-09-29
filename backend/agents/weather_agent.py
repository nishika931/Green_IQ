from langchain_core.messages import HumanMessage

from config.llm import llm
from tools.weather_tool import weather_tool


SYSTEM_PROMPT = """
You are the Weather Agent of Green IQ.

Your job is to answer weather-related plant-care questions
using the provided weather data and relevant plant-care
knowledge.

IMPORTANT RULES:

1. Use the provided weather data as the ONLY source for
   weather-related facts.

2. Use the provided plant-care knowledge when it is
   relevant to the user's question.

3. You may use your general AI knowledge when the provided
   information is not enough, but ONLY to fill the specific
   missing information needed to answer the user's question.

4. Never invent weather information.

5. Do not add unrelated plant-care information.

6. Answer ONLY the question the user asked.

7. Do NOT turn a simple question into a complete plant-care
   guide.

8. Do NOT add sections such as:
   - Practical Precautions
   - Prevention Tips
   - Watering Guide
   - Soil Guide
   - Fertilizer Guide
   - Sunlight Guide
   unless the user specifically asks for them.

9. Do NOT invent exact:
   - measurements
   - watering amounts
   - watering schedules
   - temperatures
   - humidity values
   - soil depths
   - treatment instructions

10. Do not repeat the same information.

11. Use recent conversation memory to understand references
    such as "it", "this plant", or "today".

12. Keep the answer concise, direct, and beginner-friendly.

13. If the available information is not enough to give a
    reliable answer, clearly say that more information is
    needed instead of guessing.

14. Do not mention RAG, APIs, databases, tools, agents,
    prompts, or internal processing.
"""


def weather_agent(state):

    message = state["message"]
    city = state.get("city")
    plant_name = state.get("plant_name")
    context = state.get("context", "")
    memory = state.get("memory", "")

    if not city:
        state["response"] = (
            "Please tell me your city so I can check the weather."
        )
        return state

    weather_data = weather_tool.invoke(city)

    if not weather_data or not weather_data.get("success"):
        state["response"] = (
            "Sorry, I couldn't fetch the weather information."
        )
        return state

    state["weather"] = weather_data

    prompt = f"""
{SYSTEM_PROMPT}

RECENT CONVERSATION:
{memory}

PLANT:
{plant_name}

RELEVANT PLANT-CARE KNOWLEDGE:
{context}

CURRENT WEATHER DATA:
{weather_data}

USER QUESTION:
{message}

Answer ONLY the user's question.

Use the plant-care knowledge and weather data that are
actually relevant to the question.

If some information is missing, use general knowledge
ONLY for that missing part.

Do not add unrelated advice.

Give a concise answer.
"""

    response = llm.invoke(
        [HumanMessage(content=prompt)]
    )

    state["response"] = response.content

    return state
