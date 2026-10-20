
from langchain_core.messages import HumanMessage

from config.llm import llm
from tools.perenual_tool import plant_info_tool
from tools.weather_tool import weather_tool


def plant_detail_agent(state):

    message = state["message"]
    context = state.get("context", "")
    memory = state.get("memory", "")
    city = state.get("city")
    plant_name = state.get("plant_name")

    plant_data = None
    weather_data = None

    if plant_name:
        try:
            plant_data = plant_info_tool.invoke(plant_name)
        except Exception as e:
            print(f"Plant information lookup failed: {e}")

    watering_keywords = ["water", "watering", "irrigation","schedule","plan"]

    needs_weather = any(
        keyword in message.lower()
        for keyword in watering_keywords
    )

    if needs_weather and city:
        try:
            weather_data = weather_tool.invoke(city)
            print("WATERING WEATHER DATA:", weather_data)
        except Exception as e:
            print(f"Weather tool error: {e}")

    prompt = f"""
You are Green IQ, a helpful plant-care assistant.

CURRENT USER QUESTION:
{message}

PLANT NAME:
{plant_name or "Not identified"}

RETRIEVED PLANT-CARE KNOWLEDGE:
{context}

ADDITIONAL PLANT INFORMATION:
{plant_data}

RECENT CONVERSATION:
{memory}

CURRENT WEATHER DATA:
{weather_data}

INSTRUCTIONS:
1. Answer the user's exact question directly.
2. Use retrieved Green IQ knowledge as the primary source
   for plant-care information.
3. Use additional plant information only when relevant.
4. For watering questions, use weather data when available
   alongside the plant's watering needs.
5. Consider rainfall and relevant weather conditions, but do
   not assume weather alone determines whether watering is needed.
6. Never claim to know the actual soil moisture unless the
   user provides that information.
7. If weather data is unavailable, do not invent weather conditions.
   Give useful general guidance instead.
8. If the city is missing and current weather is needed, ask the
   user for their city while still giving conditional advice.
9. If Green IQ's knowledge does not specify a detail, you may
   provide reliable general plant-care guidance without falsely
   attributing it to Green IQ.
10. Do not invent exact measurements or watering schedules and
    present them as facts from Green IQ's knowledge.
11. Use conversation memory to understand follow-up questions.
12. Avoid unrelated advice and keep the answer beginner-friendly.
13. Never mention internal processing, databases, or APIs.

Answer the current question directly.
"""

    response = llm.invoke([HumanMessage(content=prompt)])

    result = dict(state)
    result["plant_name"] = plant_name
    result["plant_data"] = plant_data
    result["weather"] = weather_data
    result["response"] = response.content

    return result
