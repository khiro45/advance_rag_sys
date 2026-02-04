from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    """The state of the agent workflow."""
    messages: Annotated[Sequence[BaseMessage], add_messages]
    context: dict
