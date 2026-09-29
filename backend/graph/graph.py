from langgraph.graph import StateGraph, END

from graph.state import AgentState

from agents.supervisor_agent import supervisor_agent
from agents.doctor_agent import doctor_agent
from agents.plant_detail_agent import plant_detail_agent
from agents.general_agent import general_agent
from agents.weather_agent import weather_agent

from ai.rag import retrieve_context


def prepare_context(state: AgentState):

    memory = state.get("memory", "")

    rag_query = f"""
Previous conversation:
{memory}

Current question:
{state["message"]}

Retrieve information specifically relevant to the plant
mentioned in the current question. Prefer plant-specific
knowledge over general knowledge or information about other
plants.
"""

    context = retrieve_context(
        rag_query,
        k=2
    )

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
