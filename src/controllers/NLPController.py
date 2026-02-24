from BaseController import BaseController
from models.Project import Project
from models.db_schemes.chunk import data_chunk
from typing import List
from stores.LLMEnums import DocumentType
class NLPController(BaseController):
    def __init__(self,vector_db_client,embedding_client,generation_client):
        super().__init__()
        self.vector_db_client=vector_db_client
        self.embedding_client=embedding_client
        self.generation_client=generation_client
    def create_collection_name(self,project_id:str):
        return f"collection_{project_id}".strip()
    def reset_vector_db_collection(self,project:Project):
        collection_name=self.create_collection_name(project_id=project.id)
        return self.vector_db_client.delete_collection(collection_name=collection_name)
    def get_vector_db_collection_info(self,project:Project):
        collection_name=self.create_collection_name(project_id=project.id)
        collection_info=self.vector_db_client.get_collection_info(collection_name=collection_name)
        return collection_info
    def index_into_vector_db(self,project:Project,chunks:List[data_chunk]):

        # step1: get collection name
        collection_name=self.create_collection_name(project_id=project.id)
        # step2: manage items
        texts=[
            chunk.chunk_text for chunk in chunks
        ]
        metadata=[
            chunk.chunk_metadata for chunk in chunks
        ]
        vectors= [
            self.embedding_client.embed_text(
                text=text,
                document_type=DocumentType.DOCUMENT.value
            )
            for text in texts
        ]

        # step3: create collection if not exists
        _=self.vector_db_client.create_collection(
            collection_name=collection_name,
            embedding_size=self.embedding_client.embedding_size,
            do_reset=do_reset
        )

        # step4: insert into vector db
        _=self.vector_db_client.insert_many(
            collection_name=collection_name,
            texts=texts,
            vectors=vectors,
            metadata=metadata   
        )
        return True
    

        