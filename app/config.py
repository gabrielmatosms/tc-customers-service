import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # SQL Database settings
    SQL_DATABASE_URL: str = os.getenv("SQL_DATABASE_URL", "postgresql://user:password@postgres:5432/customers_service")
    
    # API settings
    API_PREFIX: str = "/api/v1"


settings = Settings() 