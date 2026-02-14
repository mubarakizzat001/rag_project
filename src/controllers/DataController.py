from ..models.enums.ResponseEnum import ResponseEnum
from .BaseController import BaseController
from fastapi import UploadFile
from .ProjectController import ProjectController
import re 
import os


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

    def generate_unique_filepath(self,orig_filename:str,project_id:str):
        random_filename=self.generate_random_string()
        project_path=ProjectController().get_project_path(project_id=project_id)
        
        clean_filename=self.get_clean_file_name(orig_filename)

        new_file_path=os.path.join(
            project_path,
            random_filename + "_" + clean_filename
        )
        while os.path.exists(new_file_path):
            random_filename=self.generate_random_string()
            new_file_path=os.path.join(
                project_path,
                random_filename + "_" + clean_filename
            )
        return new_file_path, random_filename + "_" + clean_filename


    def get_clean_file_name(self, orig_file_name: str):

        # remove any special characters, except underscore and .
        cleaned_file_name = re.sub(r'[^\w.]', '', orig_file_name.strip())

        # replace spaces with underscore
        cleaned_file_name = cleaned_file_name.replace(" ", "_")

        return cleaned_file_name