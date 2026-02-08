from ..models.enums.ResponseEnum import ResponseEnum
from .BaseController import BaseController
from fastapi import UploadFile

class DataController(BaseController):
    def __init__(self):
        super().__init__()
        self.size_scale = 1024*1024
    
    def validate_upload_file(self,file:UploadFile):
        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPE:
            return False,ResponseEnum.FILE_TYPE_NOT_ALLOWED.value

        if file.size > self.app_settings.FILE_MAX_SIZE * self.size_scale:
            return False,ResponseEnum.FILE_SIZE_TOO_LARGE.value
    
        return True,ResponseEnum.FILE_UPLOADED_SUCCESSFULLY.value


    
       
