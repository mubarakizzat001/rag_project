
from .providers.QDrantDB import QDrantDB
from ...controllers.BaseController import BaseController
from .VectorEnums import VectorDBEnums
from src.helpers.config import Settings
class VectorProviderFactory:
    def __init__(self,config:Settings):
        self.config=config
        self.base_controller=BaseController()
    
    def create(self,provider:str):
        if provider == VectorDBEnums.QDRANT.value:
            db_path=self.config.VECTOR_DB_PATH
            if not db_path.startswith(("http://", "https://")):
                db_path=self.base_controller.get_database_path(db_path)
            return QDrantDB(
                db_path=db_path,
                distance_method=self.config.VECTOR_DB_DISTANCE_METHOD
                )
