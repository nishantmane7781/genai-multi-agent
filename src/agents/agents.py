from langgraph.graph import StateGraph, END
from typing import TypedDict


# -------------------
# State Definition
# -------------------
class AgentState(TypedDict):
    question: str
    dino_output: str
    marine_output: str
    earth_output: str


# -------------------
# Graph Builder
# -------------------
def build_graph(dino_rag, marine_rag, earth_rag):

    graph = StateGraph(AgentState)

    # -------------------
    # Agent Nodes
    # -------------------
    graph.add_node(
        "dino_agent",
        lambda state: {
            "dino_output": dino_rag.run(state["question"])
        }
    )

    graph.add_node(
        "marine_agent",
        lambda state: {
            "marine_output": marine_rag.run(state["question"])
        }
    )

    graph.add_node(
        "earth_agent",
        lambda state: {
            "earth_output": earth_rag.run(state["question"])
        }
    )

    # -------------------
    # Flow
    # -------------------
    graph.set_entry_point("dino_agent")
    graph.add_edge("dino_agent", "marine_agent")
    graph.add_edge("marine_agent", "earth_agent")
    graph.add_edge("earth_agent", END)

    return graph.compile()
