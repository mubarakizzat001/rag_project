from pydantic_settings import BaseSettings,SettingsConfigDict



class Settings(BaseSettings):
    App_name:str
    App_version:str
    
    FILE_ALLOWED_TYPE:list[str]
    FILE_MAX_SIZE:int
    FILE_DEFAULT_CHUNK_SIZE:int

    MONGODB_URL:str
    MONGODB_DATABASE:str

    model_config=SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

def get_settings():
    return Settings()
