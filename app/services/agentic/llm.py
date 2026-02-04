from langchain_google_genai import ChatGoogleGenerativeAI
from app.configs.config import settings

try:
    llm = ChatGoogleGenerativeAI(
        model=settings.agentic.MODEL_NAME, 
        api_key=settings.agentic.GEMINI_API_KEY,
        temperature=settings.agentic.TEMPERATURE
    )
except Exception as e:
    raise Exception(f"Error in LLM initialization: {e}")

__all__ = ["llm"]
