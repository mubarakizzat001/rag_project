from .BaseDataModel import BaseDataModel
from .enums.DataBaseenum import DataBaseEnum
from .db_schemes.project import project
class ProjectModel(BaseDataModel):
    def __init__(self,db_client:object):
        super().__init__(db_client)
        self.collection=self.db_client[DataBaseEnum.COLLECTION_PROJECT_NAME.value]

    async def create_project(self,project_instance:project):
        result = await self.collection.insert_one(project_instance.model_dump(by_alias=True,exclude_unset=True))
        project_instance._id=result.inserted_id
        return project_instance
        

    async def get_project_or_create_project(self,project_id:str):
        record = await self.collection.find_one({
            "project_id":project_id
        })
        if record is None:
            #create project
            project_instance = project(project_id=project_id)
            project_instance = await self.create_project(project_instance)
            return project_instance
        return project(**record)

    async def get_all_projects(self,page:int=1,page_size:int=10):
        #count totall of documents
        total_documents=await self.collection.count_documents({})
        #calculate total pages
        total_pages=total_documents//page_size
        if total_documents%page_size!=0:
            total_pages+=1
        cursor=self.collection.find({}).skip((page-1)*page_size).limit(page_size)

        projects=[]
        async for project in cursor:
            projects.append(
                project(**project)
            )    
        return projects,total_pages
        