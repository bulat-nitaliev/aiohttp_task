from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base, TimestampMixin


class ImageModel(Base, TimestampMixin):

    original_filename: Mapped[str] = mapped_column(String, nullable=False)
    content_type: Mapped[str] = mapped_column(String, nullable=False)
    size: Mapped[int] = mapped_column(Integer, nullable=False)
    minio_object_name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    compression_params: Mapped[str] = mapped_column(
        String, nullable=True
    )  # JSON string
