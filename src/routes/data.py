from ..helpers.config import get_settings,Settings
from fastapi import APIRouter,Depends,UploadFile,status
from fastapi.responses import JSONResponse

from ..controllers import DataController,ProjectController
import os
import aiofiles
import logging

logger=logging.getLogger("uvicorn.error")

data_router= APIRouter(prefix="/data",tags=["data"])



@data_router.post("/upload/{filename}")
async def upload_file(filename:str,file:UploadFile,
                      settings:Settings=Depends(get_settings)):
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

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message":"File uploaded successfully",
            "file_id":file_id
        }
    )
