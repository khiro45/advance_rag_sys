import langchain
from .state import SubQueryState, SubQuery
from app.services.agentic.core import prompt_loader
from app.services.agentic.llm import llm
import mlflow


def create_sub_queries(state: SubQueryState) -> SubQueryState:
    query = state["user_query"]
    prompt = prompt_loader("sub_queries_agent", {"query": query})
    structured_output = llm.with_structured_output(list[SubQuery])
    sub_queries = structured_output.invoke(prompt)
    return {"user_query": query, "sub_queries": sub_queries}