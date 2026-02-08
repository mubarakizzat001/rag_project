from ..helpers.config import get_settings,Settings
from fastapi import APIRouter,Depends,UploadFile,status
from fastapi.responses import JSONResponse

from ..controllers import DataController

data_router= APIRouter(prefix="/data",tags=["data"])



@data_router.post("/upload/{filename}")
async def upload_file(filename:str,file:UploadFile,
                      Settings:Settings=Depends(get_settings)):
    is_valid,resp = DataController().validate_upload_file(file=file)
    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "message":resp
            }
        )
    
                            

