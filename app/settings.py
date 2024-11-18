from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    db_path: str = "scraped_data.db"
    redis_url: str = "redis://localhost"
    auth_token: str = "1234"
    json_path: str = "scraped_data.json"
