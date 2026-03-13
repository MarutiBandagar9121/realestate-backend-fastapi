from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    DEBUG: bool = False

    # Tell Pydantic to read from a .env file
    model_config = SettingsConfigDict(env_file=".env")

# Create a single instance to use across the app
settings = Settings()