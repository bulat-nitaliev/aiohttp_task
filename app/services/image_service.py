from repositories.image_repo import ImageRepository
from services.minio_service import MinioService
from utils.image_processor import ImageProcessor
from utils.logging import logger
from schemas.image import ImageCreate, ImageResponse, ImageUploadResponse
from config import settings
from dataclasses import dataclass
from typing import Optional
import uuid
import json

@dataclass
class ImageService:
    image_repo: ImageRepository
    minio_service: MinioService
    processor: ImageProcessor = ImageProcessor()
    
    async def process_and_save_image(
        self, 
        file_data: bytes, 
        filename: str, 
        content_type: str, 
        compression_params: Optional[dict] = None
    ) -> ImageUploadResponse:
        try:
            # Генерация уникального имени файла
            file_extension = "jpg"
            object_name = f"{uuid.uuid4().hex}.{file_extension}"
            
            # Обработка изображения
            processed_image = await self.processor.process_image(
                file_data, compression_params
            )
            
            # Загрузка в MinIO
            await self.minio_service.upload_image(processed_image, object_name)
            
            # Сохранение метаданных в БД
            image_data = ImageCreate(
                original_filename=filename,
                content_type="image/jpeg",
                size=len(processed_image),
                minio_object_name=object_name,
                compression_params=json.dumps(compression_params) if compression_params else None
            )
            
            image = await self.image_repo.create_image(image_data)
            
            return ImageUploadResponse(
                id=image.id,
                message="Image processed and saved successfully",
                minio_object_name=object_name
            )
            
        except Exception as e:
            logger.error(
                f"Error processing image: {e}",
                extra={"route": "/upload", "functionName": "process_and_save_image"}
            )
            raise
    
    async def get_image(self, image_id: int) -> Optional[tuple[bytes, str]]:
        try:
            image = await self.image_repo.get_image_by_id(image_id)
            if not image:
                return None, None
            
            image_data = await self.minio_service.get_image(image.minio_object_name)
            return image_data, image.content_type
            
        except Exception as e:
            logger.error(
                f"Error retrieving image: {e}",
                extra={"route": "/images/{id}", "functionName": "get_image"}
            )
            raise