from langgraph.graph import StateGraph, END

from graph.state import AgentState

from agents.supervisor_agent import supervisor_agent
from agents.doctor_agent import doctor_agent
from agents.plant_detail_agent import plant_detail_agent
from agents.general_agent import general_agent
from agents.weather_agent import weather_agent


def route(state: AgentState):
    return state["intent"]


def build_graph():

    workflow = StateGraph(AgentState)

    # Nodes
    workflow.add_node("supervisor", supervisor_agent)
    workflow.add_node("doctor", doctor_agent)
    workflow.add_node("search", plant_detail_agent)
    workflow.add_node("weather", weather_agent)
    workflow.add_node("general", general_agent)

    # Entry
    workflow.set_entry_point("supervisor")

    # Routing
    workflow.add_conditional_edges(
        "supervisor",
        route,
        {
            "doctor": "doctor",
            "search": "search",
            "weather": "weather",
            "general": "general"
        }
    )

    # End nodes
    workflow.add_edge("doctor", END)
    workflow.add_edge("search", END)
    workflow.add_edge("weather", END)
    workflow.add_edge("general", END)

    return workflow.compile()


graph = build_graph()


def run_graph(state: AgentState):
    return graph.invoke(state)