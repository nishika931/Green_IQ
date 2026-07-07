from langchain_core.messages import HumanMessage

from config.llm import llm
from tools.weather_tool import weather_tool


SYSTEM_PROMPT = """
You are the Weather Agent for Green IQ.

Your job:
- Help users decide plant watering based on weather.
- Use weather data only from tool.
- Give clear watering advice.

Rules:
- If city is missing, ask user for city in response.
- If weather is available, analyze:
  - temperature
  - humidity
  - rain
  - wind
- Then decide:
  - Water today OR Not needed

Be short and practical.
"""


def weather_agent(state):

    message = state["message"]
    city = state.get("city")


    if not city:
        state["response"] = "Please tell me your city so I can check weather for your plants."
        return state

  
    weather_data = weather_tool.invoke(city)

    state["city"] = city
    state["weather"] = weather_data

    if not weather_data.get("success"):
        state["response"] = "Sorry, I couldn't fetch weather data for your city."
        return state


    response = llm.invoke([
        HumanMessage(
            content=f"""
{SYSTEM_PROMPT}

Weather Data:
{weather_data}

User Question:
{message}

Give final watering advice.
"""
        )
    ])

    state["response"] = response.content

    return state