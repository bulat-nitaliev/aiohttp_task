from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from repositories.user_repo import UserRepository
from schemas.user import  UserCreate
from models.user import UserModel
from schemas.token import  TokenPayload
from config import settings
from dataclasses import dataclass
from aiohttp import web
import aiohttp

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@dataclass
class AuthService:
    user_repo: UserRepository
    
    def create_access_token(self, subject: int, expires_delta: Optional[timedelta] = None) -> str:
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
            )
        
        to_encode = {"exp": expire, "sub": str(subject)}
        encoded_jwt = jwt.encode(
            to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
        )
        return encoded_jwt
    
    async def authenticate_user(self, username: str, password: str) -> Optional[UserModel]:
        user = await self.user_repo.get_by_username(username)
        if not user or not user.verify_password(password):
            return None
        return user
    
    async def get_current_user(self, request: web.Request) -> UserModel:
        token = self.extract_token_from_request(request)
        if not token:
            raise web.HTTPUnauthorized(reason="Not authenticated")
        
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            token_data = TokenPayload(**payload)
        except JWTError:
            raise web.HTTPUnauthorized(reason="Invalid token")
        
        user = await self.user_repo.get_by_id(int(token_data.sub))
        if not user:
            raise web.HTTPUnauthorized(reason="User not found")
        
        return user
    
    async def auth_required(self, request: web.Request) -> None:
        await self.get_current_user(request)
    
    def extract_token_from_request(self, request: web.Request) -> Optional[str]:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            return auth_header.split(" ")[1]
        return None
    
    async def register_user(self, user_data: UserCreate) -> UserModel:
        # Проверяем, существует ли пользователь
        existing_user = await self.user_repo.get_by_username(user_data.username)
        if existing_user:
            raise web.HTTPConflict(reason="Username already registered")
        
        existing_email = await self.user_repo.get_by_email(user_data.email)
        if existing_email:
            raise web.HTTPConflict(reason="Email already registered")
        
        return await self.user_repo.create(user_data)