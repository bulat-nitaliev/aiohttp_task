from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ImageCompressionParams(BaseModel):
    quality: Optional[int] = Field(None, ge=1, le=100)
    x: Optional[int] = Field(None, gt=0)
    y: Optional[int] = Field(None, gt=0)

class ImageCreate(BaseModel):
    original_filename: str
    content_type: str
    size: int
    minio_object_name: str
    compression_params: Optional[str] = None

class ImageResponse(BaseModel):
    id: int
    original_filename: str
    content_type: str
    size: int
    minio_object_name: str
    compression_params: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ImageUploadResponse(BaseModel):
    id: int
    message: str
    minio_object_name: str