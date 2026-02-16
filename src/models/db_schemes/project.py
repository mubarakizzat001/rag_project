from pydantic import BaseModel,Field,ConfigDict
from typing import Optional
from bson.objectid import ObjectId


class project(BaseModel):
    id:Optional[ObjectId]=Field(default=None,alias="_id")
    project_id:str= Field(...,min_length=1)


    model_config = ConfigDict(arbitrary_types_allowed=True)


    @classmethod
    def get_indexes(cls):
        return [{
            "key":[
                ("project_id",1)
            ],
            "name":"index_project_id_1",
            "unique":True
        }]




    