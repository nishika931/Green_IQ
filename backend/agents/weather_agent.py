from langchain_core.messages import HumanMessage

from config.llm import llm
from tools.weather_tool import weather_tool


SYSTEM_PROMPT = """
You are the Weather Agent of Green IQ.

Your job is to provide weather-based plant care advice.

Responsibilities:
- Use ONLY the weather data provided.
- Analyze temperature, humidity, rainfall, wind, and weather condition.
- Recommend whether the plant should be watered today.
- Explain why.
- Give practical precautions if needed.

Never invent weather information.
Keep the response simple and beginner-friendly.
"""


def weather_agent(state):

    message = state["message"]
    city = state.get("city")
    plant_name = state.get("plant_name")

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

    response = llm.invoke([
        HumanMessage(
            content=f"""
{SYSTEM_PROMPT}

Plant:
{plant_name}

Weather Data:
{weather_data}

User Question:
{message}

Generate a clear weather-based plant care recommendation.
"""
        )
    ])

    state["response"] = response.content

    return state