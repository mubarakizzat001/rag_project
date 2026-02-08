from fastapi import APIRouter
import os
router= APIRouter()


@router.get("/welcome")
def welcome():
    app_name=os.getenv("APP_NAME")
    app_version=os.getenv("APP_VERSION")
    return {
        "app_name": app_name,
        "app_version": app_version
    }


    