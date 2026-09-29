from langchain_core.messages import HumanMessage

from config.llm import llm
from tools.weather_tool import weather_tool


def doctor_agent(state):

    message = state["message"]
    context = state.get("context", "")
    memory = state.get("memory", "")
    city = state.get("city")

    weather_data = None

    if city:
        try:
            weather_data = weather_tool.invoke(city)
        except Exception:
            weather_data = None

    check_prompt = f"""
You are checking whether the provided plant-care knowledge
contains enough information to answer the user's question.

USER QUESTION:
{message}

PLANT-CARE KNOWLEDGE:
{context}

Rules:

- Return YES if the knowledge contains enough information
  to answer the user's question.
- Return NO if important information is missing.
- Do not use your general knowledge for this decision.
- Only judge the information explicitly present above.

Return ONLY:
YES
or
NO
"""

    check_response = llm.invoke(
        [HumanMessage(content=check_prompt)]
    )

    rag_sufficient = (
        check_response.content.strip().upper() == "YES"
    )

    if rag_sufficient:

        strict_prompt = f"""
You are Green IQ Plant Doctor.

Answer the user's question using ONLY the provided
plant-care knowledge.

USER QUESTION:
{message}

PROVIDED PLANT-CARE KNOWLEDGE:
{context}

IMPORTANT RULES:

1. Use ONLY information explicitly contained in the
   provided knowledge.

2. Do NOT add information from your general knowledge.

3. Do NOT add exact measurements, temperatures,
   percentages, dosages, schedules, treatments,
   fertilizer recommendations, or other details unless
   they are explicitly present in the provided knowledge.

4. Do NOT make assumptions.

5. Do NOT introduce causes that are not present in
   the provided knowledge.

6. You may organize or rephrase the provided information,
   but do not add new facts.

7. Keep the answer simple and beginner-friendly.

8. Do not mention RAG, databases, tools, APIs, or
   internal processing.

Answer the user's question now.
"""

        response = llm.invoke(
            [HumanMessage(content=strict_prompt)]
        )

    else:

        general_prompt = f"""
You are Green IQ Plant Doctor.

The Green IQ plant-care knowledge does not contain enough
information to completely answer the user's question.

You may now use your general AI knowledge.

USER QUESTION:
{message}

AVAILABLE GREEN IQ KNOWLEDGE:
{context}

RECENT CONVERSATION:
{memory}

WEATHER DATA:
{weather_data}

Rules:

1. Use the available Green IQ knowledge where relevant.

2. You may supplement missing information with your
   general AI knowledge.

3. Clearly avoid pretending that general knowledge came
   from the Green IQ knowledge base.

4. Do not invent weather information.

5. Do not give highly specific measurements, dosages,
   schedules, or treatment instructions unless you have
   sufficient reliable information.

6. Keep the answer beginner-friendly.

7. Do not mention RAG, databases, tools, APIs, or
   internal processing.

Answer the user's question now.
"""

        response = llm.invoke(
            [HumanMessage(content=general_prompt)]
        )

    state["weather"] = weather_data
    state["response"] = response.content

    return state