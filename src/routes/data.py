from src.models.enums.AssetTypeEnum import AssetTypeEnum
from src.models.db_schemes.chunk import data_chunk
from src.models.db_schemes.asset import Asset
from ..helpers.config import get_settings,Settings
from fastapi import APIRouter,Depends,UploadFile,status,Request
from fastapi.responses import JSONResponse

from src.models.ChunkModel import ChunkModel
from ..controllers import DataController,ProjectController,ProcessController
from ..models.ProjectModel import ProjectModel
from ..models.AssetModel import AssetModel
from ..models.enums.ResponseEnum import ResponseEnum
import os
import aiofiles
import logging
from src.routes.schemes.data import process_request
logger=logging.getLogger("uvicorn.error")

data_router= APIRouter(prefix="/data",tags=["data"])



@data_router.post("/upload/{filename}")
async def upload_file(request:Request,filename:str,file:UploadFile,
                      settings:Settings=Depends(get_settings)):

    project_model=await ProjectModel.create_instance(
        db_client=request.app.state.db
    )
    project= await project_model.get_project_or_create_project(
        project_id=filename
    )
    is_valid,resp = DataController().validate_upload_file(file=file)
    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "message":resp
            }
        )

    project_path=ProjectController().get_project_path(project_id=filename)

    file_path,file_id=DataController().generate_unique_filepath(orig_filename=file.filename,project_id=filename)     
    try:
        async with aiofiles.open(file_path,"wb") as f:
            while chunk := await file.read(settings.FILE_DEFAULT_CHUNK_SIZE):
                await f.write(chunk)
    except Exception as e:
        logger.error(f"Error uploading file: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "message":str(e)
            }
        )
    asset_model=await AssetModel.create_instance(
        db_client=request.app.state.db
    )
    asset_resource=Asset(
        asset_project_id=project.id,
        asset_type=AssetTypeEnum.FILE.value,
        asset_name=file_id,
        asset_size=os.path.getsize(file_path)

    )
    asset_record= await asset_model.create_asset(
        asset=asset_resource
    )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message":"File uploaded successfully",
            "file_id":str(asset_record.id)
        }
    )





@data_router.post("/process/{project_id}")
async def process_file(request:Request,project_id:str,process_request:process_request):
    file_id=process_request.file_id
    chunk_size=process_request.chunk_size
    chunk_overlap=process_request.overlap_size
    do_reset=process_request.do_reset

    project_model=await ProjectModel.create_instance(
        db_client=request.app.state.db
    )

    project= await project_model.get_project_or_create_project(
        project_id=project_id
    )

    process_controller=ProcessController(project_id=project_id)

    file_content=process_controller.get_file_content(file_id=file_id)

    file_chunks=process_controller.process_file_content(
        file_content=file_content,
        file_id=file_id,
        chunk_size=chunk_size,
        overlap_size=chunk_overlap
    )

    if file_chunks is None or len(file_chunks)==0:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "message":ResponseEnum.PROCESS_ERROR.value
            }
        )
    
    file_chunks_record=[
       data_chunk(
        chunk_text=chunk.page_content,
        chunk_metadata=chunk.metadata,
        chunk_order=i,
        chunk_project_id=project.id
       )


        for i,chunk in enumerate(file_chunks)

    ]

    chunk_model = await ChunkModel.create_instance(
        db_client=request.app.state.db
    )
    if do_reset == 1:
        await chunk_model.delete_chunk_by_project_id(
            project_id=project.id
        )

    no_record= await chunk_model.insert_many_chunks(file_chunks_record)


    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message":ResponseEnum.PROCESS_SUCCESS.value,
            "no_record":no_record
        }
    )



