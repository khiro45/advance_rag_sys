from langchain_core.tools import tool
from app.services.vectore_store import vs_service

@tool
def search_vector_db(query: str):
    """Search the local vector database for relevant information."""
    return vs_service.search(query, n_results=3)

@tool
def get_datetime():
    """Get the current date and time."""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# List of tools to be used by agents
tools = [search_vector_db, get_datetime]
