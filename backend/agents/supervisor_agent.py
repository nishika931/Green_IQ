from langchain_core.messages import HumanMessage

from config.llm import llm


SUPERVISOR_PROMPT = """
You are the Supervisor Agent of Green IQ.

Your job is ONLY to classify the user's message into exactly ONE
of these four intents:

doctor
plant
weather
general


========================
GENERAL INTENT
========================

Choose GENERAL when the user is:

- Greeting the assistant
- Introducing themselves
- Starting a conversation
- Having casual conversation
- Saying hello, hi, hey, good morning, etc.
- Saying they are new to gardening
- Saying they are a beginner
- Asking for general conversation without a specific plant-care question
- Asking "how are you?"
- Saying "I need help"
- Saying "I'm new here"
- Saying "I want to learn gardening" without asking a specific
  plant-care question

Examples:

"Hi"
→ general

"Hello"
→ general

"Hi, I am new to gardening"
→ general

"I am a beginner gardener"
→ general

"I want to learn gardening"
→ general

"How are you?"
→ general

"Can you help me?"
→ general


========================
DOCTOR INTENT
========================

Choose DOCTOR when the user describes a plant problem,
symptom, abnormal condition, damage, disease, pest, or asks
why something is happening to a plant.

Examples:

"Why are my leaves yellow?"
→ doctor

"My rose has brown leaves"
→ doctor

"My plant is wilting"
→ doctor

"There are insects on my plant"
→ doctor

"Why are the leaves curling?"
→ doctor

"My tomato plant has spots"
→ doctor

"Could overwatering be causing this?"
→ doctor


========================
WEATHER INTENT
========================

Choose WEATHER when the user asks about:

- Current weather
- Weather in a location
- Rain
- Temperature
- Humidity
- Weather conditions
- Whether today's weather affects watering
- Whether the plant should be watered based on current weather

Examples:

"What is the weather today?"
→ weather

"Will it rain today?"
→ weather

"Should I water my plant today?"
→ weather

"Is today's humidity important for watering?"
→ weather


========================
PLANT INTENT
========================

Choose PLANT when the user asks for normal plant information
or plant-care information without describing a problem.

Examples:

"Tell me about rose plants"
→ plant

"What light does a money plant need?"
→ plant

"How do I care for a snake plant?"
→ plant

"What soil is good for tomatoes?"
→ plant

"How should I care for my rose?"
→ plant


========================
IMPORTANT PRIORITY RULE
========================

1. Casual greeting/introduction → GENERAL

2. Plant symptom/problem → DOCTOR

3. Current weather/watering based on weather → WEATHER

4. Normal plant information/care → PLANT


IMPORTANT:

The presence of words like "plant", "gardening", "garden",
"rose", or "care" does NOT automatically mean PLANT.

For example:

"Hi, I am new to gardening"
→ GENERAL

"I want to learn about gardening"
→ GENERAL

"Tell me how to care for roses"
→ PLANT

"My rose leaves are turning yellow"
→ DOCTOR


Return ONLY one lowercase word:

doctor
plant
weather
general
"""


def supervisor_agent(state):

    message = state["message"]
    memory = state.get("memory", "")

    prompt = f"""
{SUPERVISOR_PROMPT}

Recent conversation:
{memory}

CURRENT USER MESSAGE:
{message}

Classify the message.

Return ONLY ONE word:
doctor
plant
weather
general
"""

    response = llm.invoke(
        [HumanMessage(content=prompt)]
    )

    intent = response.content.strip().lower()
    intent = intent.replace("`", "").strip()

    if intent not in [
        "doctor",
        "plant",
        "weather",
        "general"
    ]:
        intent = "general"

    state["intent"] = intent

    return state
