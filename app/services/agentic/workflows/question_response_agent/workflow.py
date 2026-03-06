from app.services.agentic.llm import llm
from .state import QuestionResponseState


def chatbot(state: QuestionResponseState):
    """Simple chatbot node that uses retrieved context to answer the user query."""
    messages = state["messages"]
    docs = state.get("docs", [])
    
    context = "\n\n".join([doc.get("doc", str(doc)) for doc in docs])
    
    system_message = {
        "role": "system",
        "content": f"You are a helpful RAG assistant. Answer the user question based ONLY on the following context:\n\n{context}"
    }
    
    # Prepend system message to conversation history
    full_messages = [system_message] + list(messages)
    
    response = llm.invoke(full_messages)
    return {"messages": [response]}