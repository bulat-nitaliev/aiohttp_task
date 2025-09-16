from PIL import Image
from io import BytesIO
import asyncio


class ImageProcessor:
    async def process_image(self, image_data: bytes, params: dict = None) -> bytes:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None, self._process_image_sync, image_data, params
        )

    def _process_image_sync(self, image_data: bytes, params: dict) -> bytes:
        image = Image.open(BytesIO(image_data))

        # Конвертация в JPEG если нужно
        if image.format != "JPEG":
            image = image.convert("RGB")

        # Применение параметров компрессии
        if params:
            if "x" in params or "y" in params:
                x = params.get("x", image.width)
                y = params.get("y", image.height)
                image = image.resize((x, y), Image.LANCZOS)

            quality = params.get("quality", 85)
        else:
            quality = 85

        # Сохранение в буфер
        output = BytesIO()
        image.save(output, format="JPEG", quality=quality, optimize=True)
        output.seek(0)

        return output.getvalue()
