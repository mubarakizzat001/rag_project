

from .routes.router import router 
from .routes.data import data_router
from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference


app= FastAPI()

app.include_router(router)
app.include_router(data_router)




@app.get("/scalar",include_in_schema=False)
def scalar():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API Reference"
    )




