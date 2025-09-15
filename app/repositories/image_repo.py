from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.image import ImageModel
from schemas.image import ImageCreate
from typing import Optional
from dataclasses import dataclass

@dataclass
class ImageRepository:
    session: AsyncSession
    
    async def create_image(self, image_data: ImageCreate) -> ImageModel:
        image = ImageModel(**image_data.model_dump())
        async with self.session:
            self.session.add(image)
            await self.session.commit()
            await self.session.refresh(image)
            return image
    
    async def get_image_by_id(self, image_id: int) -> Optional[ImageModel]:
        result = await self.session.execute(
            select(ImageModel).where(ImageModel.id == image_id)
        )
        return result.scalar_one_or_none()