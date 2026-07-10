import uuid
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Enum as SAEnum, Text
from sqlalchemy.sql import func
from enum import Enum
from ..core.database import Base


class ProcessingStatus(str, Enum):
    UPLOADED = "uploaded"
    PROCESSING = "processing"
    READY = "ready"
    FAILED = "failed"


class Document(Base):
    __tablename__ = "documents"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    filename = Column(String, nullable=False)
    original_filename = Column(String, nullable=False)
    file_size = Column(Integer, nullable=False)
    mime_type = Column(String, nullable=False)
    storage_path = Column(String, nullable=False)
    processing_status = Column(
        SAEnum(ProcessingStatus, values_callable=lambda obj: [e.value for e in obj]),
        nullable=False,
        default=ProcessingStatus.UPLOADED,
        server_default=ProcessingStatus.UPLOADED.value,
    )
    page_count = Column(Integer, nullable=True)
    word_count = Column(Integer, nullable=True)
    character_count = Column(Integer, nullable=True)
    extracted_text = Column(Text, nullable=True)
    processed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
