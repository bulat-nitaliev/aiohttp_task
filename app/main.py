from aiohttp import web
from api.routes import upload_image, get_image, login, register, get_current_user
from api.middleware import auth_middleware
# from database import init_db, close_db
# from config import settings

async def create_app():
    # app = web.Application(middlewares=[auth_middleware])
    app = web.Application()
    
    # Инициализация БД
    # app.on_startup.append(init_db)
    # app.on_cleanup.append(close_db)
    
    # Роуты
    app.router.add_post('/api/login', login)
    app.router.add_post('/api/register', register,)
    app.router.add_get('/api/me', get_current_user)
    app.router.add_post('/api/upload', upload_image)
    app.router.add_get('/api/images/{id}', get_image)
    
    return app

if __name__ == '__main__':
    web.run_app(create_app(), port=8080)