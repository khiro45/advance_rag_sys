from pydantic_settings import BaseSettings, SettingsConfigDict

class AgenticSettings(BaseSettings):
    # LLM Settings
    GEMINI_API_KEY: str = "your-gemini-key"
    MODEL_NAME: str = "gemini-2.0-flash" # Supporting latest flash models
    TEMPERATURE: float = 0.7
    
    # Agent Settings
    MAX_ITERATIONS: int = 10
    
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        env_prefix="AGENT_"
    )

agent_settings = AgenticSettings()
