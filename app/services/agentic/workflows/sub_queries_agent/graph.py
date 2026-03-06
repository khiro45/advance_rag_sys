from langgraph.graph import END, START, StateGraph
from .state import SubQueryState
from .workflow import create_sub_queries

graph = StateGraph(SubQueryState)

graph.add_node("create_sub_queries", create_sub_queries)

graph.add_edge(START, "create_sub_queries")
graph.add_edge("create_sub_queries", END)

sub_queries_agent = graph.compile()