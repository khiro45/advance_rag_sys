from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
import os 
from  dotenv import load_dotenv 
from app.configs.config import settings


try:
    llm = ChatGoogleGenerativeAI(
        model=settings.agentic.MODEL_NAME, 
        api_key=settings.agentic.GEMINI_API_KEY
    )
except Exception as e:
    raise Exception(f"Error in LLM initialization: {e}")

    