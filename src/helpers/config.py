from pydantic_settings import BaseSettings,SettingsConfigDict



class settings(BaseSettings):
    App_name:str
    App_version:str
    


    model_config=SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

def get_settings():
    return settings()


