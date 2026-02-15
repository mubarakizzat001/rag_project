

from .routes.router import router 
from .routes.data import data_router
from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference
from .helpers.config import get_settings
from motor.motor_asyncio import AsyncIOMotorClient
from contextlib import asynccontextmanager



@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()

    app.state.db_client = AsyncIOMotorClient(settings.MONGODB_URL)
    app.state.db = app.state.db_client[settings.MONGODB_DATABASE]

    yield

    app.state.db_client.close()

app = FastAPI(lifespan=lifespan)

app.include_router(router)
app.include_router(data_router)




@app.get("/scalar",include_in_schema=False)
def scalar():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API Reference"
    )




