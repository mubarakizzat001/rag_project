from ..helpers.config import get_settings
from fastapi import APIRouter

router= APIRouter()


@router.get("/welcome")
def welcome():
    s_settings=get_settings()
    app_name=s_settings.App_name
    app_version=s_settings.App_version
    return {
        "app_name": app_name,
        "app_version": app_version
    }


    