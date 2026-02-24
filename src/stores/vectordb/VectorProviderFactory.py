
from .providers.QDrantDB import QDrantDB
from ...controllers.BaseController import BaseController
from .VectorEnums import VectorDBEnums
class VectorProviderFactory:
    def __init__(self):
        self.config=config
        self.base_controller=BaseController()
    
    def create(self,provider:str):
        if provider == VectorDBEnums.QDRANT:
            db_path=self.base_controller.get_database_path(self.config.VECTOR_DB_PATH)
            return QDrantDB(
                db_path=db_path,
                distance_method=self.config.VECTOR_DB_DISTANCE_METHOD
                )
