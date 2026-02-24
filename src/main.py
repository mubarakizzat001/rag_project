

from src.routes.nlp import nlp_router
from .routes.router import router 
from .routes.data import data_router
from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference
from .helpers.config import get_settings
from motor.motor_asyncio import AsyncIOMotorClient
from contextlib import asynccontextmanager
from src.stores.llm.LLMProviderFactory import LLMProviderFactory
from src.stores.vectordb.VectorProviderFactory import VectorProviderFactory


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()

    app.state.db_client = AsyncIOMotorClient(settings.MONGODB_URL)
    app.state.db = app.state.db_client[settings.MONGODB_DATABASE]

    llm_provider_factory=LLMProviderFactory(settings)
    vector_provider_factory=VectorProviderFactory(settings)
    #generation client
    app.state.generation_client = llm_provider_factory.create(settings.GENERATION_BACKEND)
    app.state.generation_client.set_generate_model(settings.GENERATION_MODEL_ID)
    #embedding client
    app.state.embedding_client = llm_provider_factory.create(settings.EMBEDDING_BACKEND)
    app.state.embedding_client.set_embedding_model(settings.EMBEDDING_MODEL_ID,settings.EMBEDDING_MODEL_SIZE)
    #vector db client
    app.state.vector_db_client = vector_provider_factory.create(settings.VECTOR_DB_BACKEND)
    app.state.vector_db_client.connect()

    yield
    
    app.state.db_client.close()

app = FastAPI(lifespan=lifespan)

app.include_router(router)
app.include_router(data_router)
app.include_router(nlp_router)



@app.get("/scalar",include_in_schema=False)
def scalar():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API Reference"
    )




