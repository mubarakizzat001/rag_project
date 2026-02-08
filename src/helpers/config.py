from pydantic_settings import BaseSettings,SettingsConfigDict



class Settings(BaseSettings):
    App_name:str
    App_version:str
    
    FILE_ALLOWED_TYPE:list[str]
    FILE_MAX_SIZE:int


    model_config=SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

def get_settings():
    return Settings()

settings=get_settings()
print(settings.FILE_ALLOWED_TYPE)
