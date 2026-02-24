from pydantic_settings import BaseSettings,SettingsConfigDict



class Settings(BaseSettings):
    App_name:str
    App_version:str
    
    FILE_ALLOWED_TYPE:list[str]
    FILE_MAX_SIZE:int
    FILE_DEFAULT_CHUNK_SIZE:int

    MONGODB_URL:str
    MONGODB_DATABASE:str

    GENERATION_MODEL_ID:str=None
    EMBEDDING_MODEL_ID:str=None
    EMBEDDING_MODEL_SIZE:int=None

    default_input_max_charecters:int=None
    default_output_max_tokens:int=None
    default_temperature:float=None


    GENERATION_BACKEND:str
    EMBEDDING_BACKEND:str

   
    VECTOR_DB_BACKEND:str
    VECTOR_DB_PATH:str
    VECTOR_DB_DISTANCE_METHOD:str=None

    model_config=SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

def get_settings():
    return Settings()
