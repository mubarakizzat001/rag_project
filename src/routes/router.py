from ..helpers.config import get_settings,Settings
from fastapi import APIRouter,Depends

router= APIRouter(prefix="/welcome",tags=["welcome"])


@router.get("/")
def welcome(settings:Settings=Depends(get_settings)):
    app_name=settings.App_name
    app_version=settings.App_version
    return {
        "app_name": app_name,
        "app_version": app_version
    }


    