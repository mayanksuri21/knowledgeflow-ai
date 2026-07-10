from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from ..models.document import ProcessingStatus


class DocumentBase(BaseModel):
    filename: str
    original_filename: str
    file_size: int
    mime_type: str
    storage_path: str
    processing_status: ProcessingStatus = ProcessingStatus.UPLOADED


class DocumentCreate(DocumentBase):
    user_id: str


class DocumentUpdate(BaseModel):
    filename: Optional[str] = None
    processing_status: Optional[ProcessingStatus] = None


class DocumentResponse(DocumentBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
