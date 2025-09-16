from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import NullPool
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from config import settings
import logging

# Настройка логирования
logger = logging.getLogger(__name__)

# Базовый класс для моделей
Base = declarative_base()

# Создание асинхронного движка
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,  # Логирование SQL-запросов (можно отключить в продакшене)
    poolclass=NullPool,  # Отключаем пул соединений для asyncpg
    future=True,  # Используем future-совместимый API
)

# Создание фабрики сессий
async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,  # Отключаем expire после commit для работы с объектами после сессии
    autoflush=False,
)


@asynccontextmanager
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Асинхронный контекстный менеджер для получения сессии БД.
    Гарантирует корректное закрытие сессии даже при возникновении исключений.
    """
    session = async_session()
    try:
        yield session
        await session.commit()
    except Exception as e:
        await session.rollback()
        logger.error(f"Database error: {e}", exc_info=True)
        raise
    finally:
        session.close()


async def init_db() -> None:
    """
    Инициализация базы данных - создание всех таблиц.
    """
    async with engine.begin() as conn:
        # Создаем все таблицы
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database initialized successfully")


async def close_db() -> None:
    """
    Корректное закрытие соединений с базой данных.
    """
    await engine.dispose()
    logger.info("Database connections closed")


# Для удобства импорта
async def async_session() -> AsyncSession:
    """
    Функция для получения асинхронной сессии (альтернатива контекстному менеджеру).
    """
    return async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)()
