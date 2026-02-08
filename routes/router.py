from fastapi import APIRouter

router= APIRouter()


@router.get("/welcome")
def welcome():

    return {
        "message": "welcome to our fastapi"
    }


    