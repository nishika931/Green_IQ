from langchain_core.messages import HumanMessage

from config.llm import llm
from tools.perenual_tool import plant_info_tool


def plant_detail_agent(state):

    message = state["message"]
    context = state.get("context", "")
    memory = state.get("memory", "")

    extract_response = llm.invoke(
        f"""
Identify the plant name mentioned in the user's message.

Recent conversation:
{memory}

User message:
{message}

If a plant is clearly mentioned, return only its common name.

If no plant is mentioned, return:
NONE
"""
    )

    plant_name = extract_response.content.strip()
    plant_name = plant_name.replace("`", "").strip()

    plant_data = None

    if plant_name and plant_name.upper() != "NONE":

        try:
            plant_data = plant_info_tool.invoke(plant_name)

        except Exception as e:
            plant_data = {
                "success": False,
                "message": str(e)
            }

    check_prompt = f"""
You are checking whether the provided Green IQ plant-care
knowledge contains enough information to answer the user's
question.

USER QUESTION:
{message}

PLANT-CARE KNOWLEDGE:
{context}

Rules:

- Return YES if the knowledge contains enough information
  to answer the user's actual question.
- Return NO only if important information needed to answer
  the actual question is missing.
- Do not require extra information that the user did not ask for.
- Judge ONLY the information explicitly present above.
- Do not use your general knowledge.

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

        prompt = f"""
You are Green IQ's Plant Detail Agent.

Answer the user's question using ONLY the provided
Green IQ plant-care knowledge.

USER QUESTION:
{message}

PLANT-CARE KNOWLEDGE:
{context}

IMPORTANT RULES:

1. Use ONLY information explicitly present in the
   provided Green IQ plant-care knowledge.

2. Do NOT add facts from general AI knowledge.

3. Answer ONLY the question that the user asked.

4. Do NOT add unrelated care tips.

5. Do NOT create a long general plant-care guide unless
   the user specifically asks for one.

6. Do NOT invent:
   - exact watering schedules
   - exact water amounts
   - exact sunlight hours
   - exact temperature ranges
   - exact humidity percentages
   - fertilizer dosages
   - soil measurements
   - treatment instructions

7. You may organize or rephrase the provided information,
   but do not add new facts.

8. Keep the answer concise and beginner-friendly.

9. Do not mention RAG, APIs, databases, tools, or
   internal processing.

Give the answer now.
"""



    else:

        prompt = f"""
You are Green IQ's Plant Detail Agent.

The provided Green IQ knowledge does not contain enough
information to completely answer the user's question.

You may use general AI knowledge ONLY to fill the
specific information that is missing.

USER QUESTION:
{message}

PLANT NAME:
{plant_name}

GREEN IQ PLANT-CARE KNOWLEDGE:
{context}

PLANT DATA:
{plant_data}

IMPORTANT RULES:

1. First use the Green IQ knowledge to answer whatever
   part of the question it can answer.

2. If information is missing, use general AI knowledge
   ONLY for the missing part.

3. Do NOT add unrelated plant-care information.

4. Do NOT turn the answer into a complete plant-care guide.

5. Answer ONLY the user's actual question.

6. Do NOT provide extra sections such as:
   - Prevention Tips
   - How to Detect
   - Fertilizing
   - Pruning
   - Sunlight
   - Temperature
   - Pet Safety
   unless the user specifically asks about them.

7. Keep the answer focused and reasonably short.

8. Do NOT invent information from Plant Data.

9. If giving general AI knowledge, keep it relevant to
   the exact question.

10. Do not give unnecessary exact measurements,
    dosages, schedules, or treatment instructions.

11. Do not repeat the same information in different ways.

12. Do not mention RAG, APIs, databases, tools, or
    internal processing.

13. If the available information is still insufficient
    to answer reliably, say that the available information
    is limited instead of guessing.

Give the answer now.
"""

    response = llm.invoke(
        [HumanMessage(content=prompt)]
    )

    state["plant_name"] = plant_name
    state["plant_data"] = plant_data
    state["response"] = response.content

    return state
