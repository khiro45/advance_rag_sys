from langgraph.graph import StateGraph, END
from app.services.agentic.workflows.state import AgentState
from app.services.agentic.llm import llm
from app.services.agentic import prompt_loader

def call_model(state: AgentState):
    messages = state["messages"]
    response = llm.invoke(messages)
    return {"messages": [response]}

prompt = prompt_loader.load_prompt("researcher", "system", topic="AI", context="...")

# Define the graph
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("agent", call_model)

# Set entry point
workflow.set_entry_point("agent")

# Add edges
workflow.add_edge("agent", END)

# Compile the graph
agent_graph = workflow.compile()
