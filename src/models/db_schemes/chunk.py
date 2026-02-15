from pydantic import BaseModel,Field,ConfigDict
from typing import Optional
from bson.objectid import ObjectId

class data_chunk(BaseModel):
    _id:Optional[ObjectId]=None
    chunk_text:str=Field(...,min_length=1)
    chunk_metadata:dict
    chunk_order:int=Field(...,ge=0)
    chunk_project_id:ObjectId






    model_config = ConfigDict(arbitrary_types_allowed=True)
        

