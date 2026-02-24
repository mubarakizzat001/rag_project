from src.routes.schemes.nlp import SearchRequest
from src.models.ChunkModel import ChunkModel
from src.controllers.NLPController import NLPController
from fastapi import APIRouter,Depends,UploadFile,status,Request
from fastapi.responses import JSONResponse
from .schemes.nlp import PushRequest
import logging
from src.models.ProjectModel import ProjectModel
logger = logging.getLogger("uvicorn.error")

nlp_router = APIRouter(
    prefix="/nlp",
    tags=["nlp"]
)

@nlp_router.post("/nlp/{project_id}")
async def index_project(request:Request,project_id:str,push_request:PushRequest):
    project_model= await ProjectModel.create_instance(
        request.app.state.db
    )
    chunk_model= await ChunkModel.create_instance(
        request.app.state.db
    )

    project = await project_model.get_project_or_create_project(
        project_id=project_id
    )
    
    if not project:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "message":"Project not found"
            }
        )
    nlp_controller=NLPController(
        vector_db_client=request.app.state.vector_db_client,
        embedding_client=request.app.state.embedding_client,
        generation_client=request.app.state.generation_client
    )

    has_records=True
    page_no=1
    inserted_items_count=0
    idx=0

    while has_records:
        records=await chunk_model.get_project_chunks(
            project_id=project.id,
            page_no=page_no
        )
        if records:
            page_no+=1

        if not records or len(records)==0:
            has_records=False
            break
        
        chunks_ids= range(idx,idx+len(records))
        idx+=len(records)

        is_inserted= await nlp_controller.index_into_vector_db(
            project=project,
            chunks=records,
            do_reset=push_request.do_reset,
            chunks_ids=chunks_ids
        ) 

        if not is_inserted:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "message":"Failed to index project"
                }
            )
        inserted_items_count+=len(records)

    return JSONResponse(
            content={
                "message":"Project indexed successfully",
                "inserted_items_count":inserted_items_count
            })




@nlp_router.get("/nlp/{project_id}")
async def get_index_project_info(request:Request,project_id:str):


    project_model= await ProjectModel.create_instance(
        request.app.state.db
    )

    project = await project_model.get_project_or_create_project(
        project_id=project_id
    )

    nlp_controller=NLPController(
        vector_db_client=request.app.state.vector_db_client,
        embedding_client=request.app.state.embedding_client,
        generation_client=request.app.state.generation_client
    )

    collection_info=nlp_controller.get_vector_db_collection_info(project=project)

    return JSONResponse(
        content={
            "message":"Project info retrieved successfully",
            "collection_info":collection_info
        }
    )

@nlp_router.post("/search/{project_id}")
async def search_project(request:Request,project_id:str,search_request:SearchRequest ):


    project_model= await ProjectModel.create_instance(
        request.app.state.db
    )

    project = await project_model.get_project_or_create_project(
        project_id=project_id
    )

    nlp_controller=NLPController(
        vector_db_client=request.app.state.vector_db_client,
        embedding_client=request.app.state.embedding_client,
        generation_client=request.app.state.generation_client
    )

    results=await nlp_controller.search_vector_db_collection(
        project=project,
        text=search_request.text,
        limit=search_request.limit
    )

    if not results:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "message":"No results found"
            }
        )
    return JSONResponse(
        content={
            "message":"Results retrieved successfully",
            "results":results
        }
    )
