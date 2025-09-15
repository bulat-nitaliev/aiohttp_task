from aiohttp import web
from aiohttp.web_request import Request
from services.image_service import ImageService
from services.auth_service import AuthService
from api.dependencies import get_image_service, get_auth_service
from schemas.user import UserCreate
from schemas.image import ImageCompressionParams
from utils.logging import logger
import json

async def login(request: Request) -> web.Response:
    auth_service = await get_auth_service(request)
    
    data = await request.json()
    username = data.get("username")
    password = data.get("password")
    
    if not username or not password:
        raise web.HTTPBadRequest(reason="Username and password required")
    
    user = await auth_service.authenticate_user(username, password)
    if not user:
        raise web.HTTPUnauthorized(reason="Incorrect username or password")
    
    access_token = auth_service.create_access_token(user.id)
    
    logger.info(
        f"User logged in: {username}",
        extra={"route": "/login", "functionName": "login"}
    )
    
    return web.json_response({
        "access_token": access_token,
        "token_type": "bearer"
    })

async def register(request: Request) -> web.Response:
    auth_service = await get_auth_service(request)
    
    data = await request.json()
    user_data = UserCreate(**data)
    
    user = await auth_service.register_user(user_data)
    
    access_token = auth_service.create_access_token(user.id)
    
    logger.info(
        f"User registered: {user.username}",
        extra={"route": "/register", "functionName": "register"}
    )
    
    return web.json_response({
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }
    })

async def get_current_user(request: Request) -> web.Response:
    auth_service = await get_auth_service(request)
    user = await auth_service.get_current_user(request)
    
    return web.json_response({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "is_active": user.is_active,
        "is_superuser": user.is_superuser
    })

# Обновленные эндпоинты для работы с изображениями
async def upload_image(request: Request) -> web.Response:
    image_service = await get_image_service(request)
    auth_service = await get_auth_service(request)
    
    # Проверка авторизации
    await auth_service.auth_required(request)
    
    # Чтение multipart данных
    reader = await request.multipart()
    compression_params = {}
    file_data = None
    filename = None
    content_type = None
    
    while True:
        field = await reader.next()
        if not field:
            break
        
        if field.name == 'file':
            file_data = await field.read()
            filename = field.filename
            content_type = field.headers.get('Content-Type')
        elif field.name in ['quality', 'x', 'y']:
            value = await field.text()
            if value.isdigit():
                compression_params[field.name] = int(value)
    
    # Валидация параметров компрессии
    if compression_params:
        try:
            ImageCompressionParams(**compression_params)
        except ValueError as e:
            return web.json_response({"error": str(e)}, status=400)
    
    # Обработка изображения
    result = await image_service.process_and_save_image(
        file_data, filename, content_type, compression_params or None
    )
    
    logger.info(
        f"Image uploaded successfully: {result.minio_object_name}",
        extra={"route": "/upload", "functionName": "upload_image"}
    )
    
    return web.json_response(result.model_dump())

async def get_image(request: Request) -> web.Response:
    image_service = await get_image_service(request)
    auth_service = await get_auth_service(request)
    
    # Проверка авторизации
    await auth_service.auth_required(request)
    
    image_id = int(request.match_info['id'])
    image_data, content_type = await image_service.get_image(image_id)
    
    if not image_data:
        return web.json_response({"error": "Image not found"}, status=404)
    
    logger.info(
        f"Image retrieved successfully: {image_id}",
        extra={"route": "/images/{id}", "functionName": "get_image"}
    )
    
    return web.Response(
        body=image_data,
        content_type=content_type
    )