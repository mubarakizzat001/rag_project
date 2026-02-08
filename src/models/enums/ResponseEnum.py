from enum import Enum

class ResponseEnum(Enum):

    FILE_TYPE_NOT_ALLOWED = "File type not allowed"
    FILE_SIZE_TOO_LARGE="File size too large"
    FILE_UPLOADED_SUCCESSFULLY="File uploaded successfully"