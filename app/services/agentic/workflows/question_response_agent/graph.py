from langgraph.graph import END, START, StateGraph
from .state import QuestionResponseState
from .workflow import chatbot

graph = StateGraph(QuestionResponseState)

graph.add_node("chatbot", chatbot)

graph.add_edge(START, "chatbot")
graph.add_edge("chatbot", END)

question_response_agent = graph.compile()