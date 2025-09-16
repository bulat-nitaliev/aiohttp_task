from minio import Minio
from minio.error import S3Error
from io import BytesIO
from config import settings
from utils.logging import logger
from dataclasses import dataclass


@dataclass
class MinioService:
    client: Minio = None

    def __post_init__(self):
        self.client = Minio(
            settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=settings.MINIO_SECURE,
        )
        self._ensure_bucket_exists()

    def _ensure_bucket_exists(self):
        try:
            if not self.client.bucket_exists(settings.MINIO_BUCKET_NAME):
                self.client.make_bucket(settings.MINIO_BUCKET_NAME)
                logger.info(f"Created bucket: {settings.MINIO_BUCKET_NAME}")
        except S3Error as e:
            logger.error(f"Error creating bucket: {e}")
            raise

    async def upload_image(self, image_data: bytes, object_name: str) -> str:
        try:
            data = BytesIO(image_data)
            self.client.put_object(
                settings.MINIO_BUCKET_NAME,
                object_name,
                data,
                len(image_data),
                content_type="image/jpeg",
            )
            return object_name
        except S3Error as e:
            logger.error(f"Error uploading to MinIO: {e}")
            raise

    async def get_image(self, object_name: str) -> bytes:
        try:
            response = self.client.get_object(settings.MINIO_BUCKET_NAME, object_name)
            return response.read()
        except S3Error as e:
            logger.error(f"Error retrieving from MinIO: {e}")
            raise
        finally:
            response.close()
            response.release_conn()
