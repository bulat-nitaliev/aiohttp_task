from aiohttp import web
from services.image_service import ImageService
from services.auth_service import AuthService
from services.minio_service import MinioService
from repositories.image_repo import ImageRepository
from repositories.user_repo import UserRepository
from database import async_session,get_db
from sqlalchemy.ext.asyncio import AsyncSession



async def get_image_repo(request: web.Request) -> ImageRepository:
    session:AsyncSession = await async_session()
    return ImageRepository(session)

async def get_user_repo(request: web.Request) -> UserRepository:
    # session = await get_db_session(request)
    session:AsyncSession = await async_session()
    return UserRepository(session=session)

async def get_minio_service(request: web.Request) -> MinioService:
    return MinioService()

async def get_image_service(request: web.Request) -> ImageService:
    repo = await get_image_repo(request)
    minio_service = await get_minio_service(request)
    return ImageService(repo, minio_service)

async def get_auth_service(request: web.Request) -> AuthService:
    user_repo = await get_user_repo(request)
    return AuthService(user_repo)