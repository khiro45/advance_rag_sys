from langgraph.graph import END, START, StateGraph
from .state import QuestionResponseState
from .workflow import chatbot  , create_sub_queries

graph = StateGraph(QuestionResponseState)

graph.add_node("sub_query" , create_sub_queries)
graph.add_node("chatbot", chatbot)

graph.add_edge(START, "create_sub_queries")
graph.add_edge("create_sub_queries", "chatbot")
graph.add_edge("chatbot", END)

question_response_agent = graph.compile()