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

    watering_keywords = [
        "water",
        "watering",
        "irrigation",
        "schedule",
        "rain",
        "rainfall",
        "weather",
        "should i water",
    ]

    needs_weather = any(
        keyword in message.lower()
        for keyword in watering_keywords
    )

    if needs_weather and city:
        try:
            weather_data = weather_tool.invoke(city)
        except Exception as e:
            print(f"Weather tool error: {e}")

   
    if isinstance(context, str):
        context = context.strip()
    else:
        context = ""

    print("\n========== PLANT KNOWLEDGE DEBUG ==========")
    print("Question:", message)
    print("Plant:", plant_name)
    print("Retrieved context:", context or "EMPTY")
    print("===========================================\n")

    prompt = f"""
You are Green IQ, a simple and reliable plant-care assistant.

USER QUESTION:
{message}

IDENTIFIED PLANT:
{plant_name or "Not identified"}

GREEN IQ KNOWLEDGE:
{context or "No relevant knowledge retrieved."}

ADDITIONAL PLANT INFORMATION:
{plant_data if plant_data else "Unavailable."}

WEATHER DATA:
{weather_data if weather_data else "Unavailable."}

RECENT CONVERSATION:
{memory or "Unavailable."}

INSTRUCTIONS:

1. First, check whether the Green IQ knowledge contains enough
   information to answer the user's question.

2. If the knowledge is sufficient, answer using ONLY the Green IQ
   knowledge. Do not add any information from general LLM knowledge
   or additional plant information.

3. If the knowledge is partially sufficient, use the available
   knowledge for the parts it answers. Use general LLM knowledge
   ONLY to fill the genuinely missing information.

4. If the knowledge is completely insufficient, answer using
   reliable general LLM knowledge.

5. Never change the meaning of the knowledge or invent additional
   recommendations when the knowledge already answers the question.

6. Do not repeat the same information in different words.

7. Include only information relevant to the user's question.

8. Use additional plant information and weather data only when
   needed to fill missing information or answer a relevant
   plant-specific or weather-related question.

9. Use conversation history only to understand follow-up questions.

10. If information is missing and you cannot answer reliably,
    clearly acknowledge the limitation instead of guessing.

11. Keep the answer simple, natural, and beginner-friendly.

Return only the answer.
"""

    response = llm.invoke([
        HumanMessage(content=prompt)
    ])

    result = dict(state)

    result["plant_name"] = plant_name
    result["plant_data"] = plant_data
    result["weather"] = weather_data
    result["response"] = response.content

    return result
