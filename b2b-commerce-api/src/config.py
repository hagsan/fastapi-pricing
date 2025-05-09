from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_USERNAME: str = "postgres"
    DATABASE_PASSWORD: str = "your_password"
    DATABASE_HOST: str = "localhost"
    DATABASE_PORT: int = 5432
    DATABASE_NAME: str = "prices_db"
    
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.DATABASE_USERNAME}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"
    
    class Config:
        env_file = ".env"
        extra = "ignore"  # Ignore extra fields

settings = Settings()
