from pydantic_settings import BaseSettings , SettingsConfigDict

class AgenticSettings(BaseSettings):
    GEMINI_API_KEY: str = "your-gemini-key"
    MODEL_NAME: str = "gemini-2.5-flash"
    TEMPERATURE: float = 0.7
    MAX_ITERATIONS: int = 10

    model_config = SettingsConfigDict(
    env_file=".env",
    extra="ignore",
    env_prefix="VS_"
    )