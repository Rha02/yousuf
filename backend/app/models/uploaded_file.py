from pydantic import BaseModel

class UploadedFile(BaseModel):
    id: str
    chat_id: str
    file_name: str
    file_size: int
    file_type: str
    uploaded_at: str