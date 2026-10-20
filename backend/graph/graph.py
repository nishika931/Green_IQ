from langgraph.graph import StateGraph, END

from graph.state import AgentState

from agents.supervisor_agent import supervisor_agent
from agents.doctor_agent import doctor_agent
from agents.plant_detail_agent import plant_detail_agent
from agents.general_agent import general_agent
from agents.weather_agent import weather_agent



import re
from pathlib import Path



def get_plant_context(message):
    file_path = (
        Path(__file__).resolve().parents[1]
        / "knowledge"
        / "plant_care.txt"
    )

    if not file_path.exists():
        print("Knowledge file not found:", file_path)
        return ""

    text = file_path.read_text(encoding="utf-8")
    sections = re.split(r"(?=^## )", text, flags=re.MULTILINE)

    question = message.lower()

    plant_aliases = {
        "tomato": ["tomato", "tomatoes"],
        "rose": ["rose", "roses"],
        "money plant": ["money plant", "pothos"],
        "snake plant": ["snake plant"],
        "aloe vera": ["aloe vera", "aloe"],
    }

    for plant, aliases in plant_aliases.items():
        if any(alias in question for alias in aliases):
            for section in sections:
                heading = section.strip().split("\n", 1)[0].lower()

                if plant in heading and (
                    "care" in heading
                ):
                    return section.strip()

    for section in sections:
        heading = section.strip().split("\n", 1)[0].lower()

        if "general plant care" in heading:
            return section.strip()

    return ""


def prepare_context(state: AgentState):
    memory = state.get("memory", "")
    message = state["message"]

    context = get_plant_context(message)

    print("\n===== FINAL KNOWLEDGE CONTEXT =====")
    print(context or "No matching section found")
    print("===================================\n")

    return {
        "memory": memory,
        "context": context
    }


def route(state: AgentState):
    return state["intent"]


def build_graph():

    workflow = StateGraph(AgentState)

    workflow.add_node("prepare_context", prepare_context)
    workflow.add_node("supervisor", supervisor_agent)
    workflow.add_node("doctor", doctor_agent)
    workflow.add_node("plant", plant_detail_agent)
    workflow.add_node("weather", weather_agent)
    workflow.add_node("general", general_agent)

    workflow.set_entry_point("prepare_context")

    workflow.add_edge(
        "prepare_context",
        "supervisor"
    )

    workflow.add_conditional_edges(
        "supervisor",
        route,
        {
            "doctor": "doctor",
            "plant": "plant",
            "weather": "weather",
            "general": "general"
        }
    )

    workflow.add_edge("doctor", END)
    workflow.add_edge("plant", END)
    workflow.add_edge("weather", END)
    workflow.add_edge("general", END)

    return workflow.compile()


graph = build_graph()


def run_graph(state: AgentState):
    return graph.invoke(state)
