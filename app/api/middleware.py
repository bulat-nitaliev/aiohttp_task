from aiohttp import web
from utils.logging import logger
from jose import jwt, exceptions
from config import settings


async def auth_middleware(app, handler):
    async def middleware_handler(request):
        if request.path.startswith("/api/"):
            token = request.headers.get("Authorization", "").replace("Bearer ", "")

            try:
                payload = jwt.decode(
                    token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
                )
                request["user_id"] = payload.get("sub")
            except Exception as e:
                print(e)
                return web.json_response({"error": "Invalid token"}, status=401)

        return await handler(request)

    return middleware_handler
