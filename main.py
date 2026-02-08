


from dotenv import load_dotenv
load_dotenv(".env")
from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference
from rag_project.routes.router import router

app= FastAPI()

app.include_router(router)




@app.get("/scalar",include_in_schema=False)
def scalar():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API Reference"
    )




