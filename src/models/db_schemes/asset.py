from pydantic import BaseModel,Field,ConfigDict
from typing import Optional
from bson.objectid import ObjectId
from datetime import datetime

class Asset(BaseModel):
    id:Optional[ObjectId]=Field(default=None,alias="_id")
    asset_project_id:ObjectId
    asset_name:str=Field(...,min_length=1)
    asset_type:str=Field(...,min_length=1)
    asset_size:int=Field(default=None,ge=0)
    asset_config:dict=Field(default=None)
    asset_pushed_at:datetime=Field(default=datetime.utcnow)



    model_config = ConfigDict(arbitrary_types_allowed=True)


    @classmethod
    def get_indexes(cls):
        return [{
            "key":[
                ("asset_project_id",1)
            ],
            "name":"index_asset_project_id_1",
            "unique":False
        },{
            "key":[
                ("asset_name",1)
            ],
            "name":"index_asset_name_1",
            "unique":True
        }]
        

