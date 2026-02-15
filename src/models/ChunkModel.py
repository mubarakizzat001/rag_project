from .BaseDataModel import BaseDataModel
from .db_schemes.chunk import data_chunk
from .enums.DataBaseenum import DataBaseEnum
from pymongo import InsertOne
from bson.objectid import ObjectId

class ChunkModel(BaseDataModel):
    def __init__(self,db_client:object):
        super().__init__(db_client)
        self.collection=self.db_client[DataBaseEnum.COLLECTION_CHUNK_NAME.value]

    async def create_chunk(self,chunk:data_chunk):
        result=await self.collection.insert_one(chunk.model_dump(by_alias=True,exclude_unset=True))
        chunk._id=result.inserted_id
        return chunk

    async def get_chunk(self,chunk_id:str):
        record= await self.collection.find_one({
            "_id":objectid(chunk_id)
        })
        if record is None:
            return None
        return data_chunk(**record)
    
    async def insert_many_chunks(self,chunk:list,batch_size:int=100):

        for i in range(0,len(chunk),batch_size):
            batch=chunk[i:i+batch_size]
            operation = [
                InsertOne(chunk.model_dump(by_alias=True,exclude_unset=True))
                for chunk in batch
            ]
            await self.collection.bulk_write(operation)
        

        return len(chunk)

    async def delete_chunk_by_project_id(self,project_id:ObjectId):
        result=await self.collection.delete_many({
            "chunk_project_id":project_id
        })

        return result.deleted_count

