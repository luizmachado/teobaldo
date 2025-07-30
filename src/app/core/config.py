from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Chave secreta para assinar os tokens JWT.
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 

    gemini_api_key: str
    openai_api_key: str
    google_maps_api_key: str
    openweather_api_key: str
    pythonpath: str
    app_title: str

    class Config:
        env_file = ".env"

settings = Settings()
