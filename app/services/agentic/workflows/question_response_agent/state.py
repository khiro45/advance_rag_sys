from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages


class QuestionResponseState(TypedDict):
    messages: Annotated[list, add_messages]
    docs: list[dict]