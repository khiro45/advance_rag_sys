from app.services.agentic.llm import llm
from .state import QuestionResponseState
from app.services.agentic.core import prompt_loader
from state import SubQuery 


def create_sub_queries(state: QuestionResponseState) -> QuestionResponseState:
    query = state["user_query"]
    prompt = prompt_loader("sub_queries_agent", {"query": query})
    structured_output = llm.with_structured_output(list[SubQuery])
    sub_queries = structured_output.invoke(prompt)
    return {"user_query": query, "sub_queries": sub_queries}


def chatbot(state: QuestionResponseState) -> QuestionResponseState:
    message = state["message"]
    docs = state['docs']
    
    prompt = prompt_loader("question_answering_agent", {"docs": docs , "message":message})
    response = llm.invoke(prompt)
    return {"message reponce": [response]}  
   