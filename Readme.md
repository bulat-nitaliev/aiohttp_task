# Image Processing API
Асинхронное API для обработки изображений с использованием Python 3.9, aiohttp, PostgreSQL и MinIO.

### 🚀 Возможности
Загрузка изображений (JPEG, PNG, GIF)

Конвертация в формат JPEG

Изменение размера и качества изображений

Хранение метаданных в PostgreSQL

Хранение файлов в MinIO (S3-совместимое хранилище)

JWT-аутентификация

Логирование операций

Полностью асинхронная архитектура

### 🛠 Технологии
Python 3.9+

aiohttp - асинхронный веб-фреймворк

PostgreSQL 14+ - база данных

MinIO - объектное хранилище

SQLAlchemy 2.0+ - ORM

Alembic - миграции базы данных

Pillow - обработка изображений

JWT - аутентификация

Docker - контейнеризация

### 📦 Установка
Требования
Docker и Docker Compose

Python 3.9+ (для локальной разработки)

Быстрый старт
Клонируйте репозиторий:

```
git clone https://github.com/bulat-nitaliev/aiohttp_task.git
cd image-processing-api
```
Создайте файл окружения:

```
cp .env.example .env
```

Запустите сервисы:

```
docker-compose up -d
```
Примените миграции базы данных:

```
docker-compose exec app alembic upgrade head
```
Приложение будет доступно по адресу: http://localhost:8080

### ⚙️ Конфигурация
Настройки приложения задаются через переменные окружения:

env
### Database
DB_HOST=postgres
DB_PORT=5432
DB_NAME=image_db
DB_USER=postgres
DB_PASSWORD=password

### Security
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

### MinIO
MINIO_ENDPOINT=minio:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_SECURE=false
MINIO_BUCKET_NAME=images

### Application
ALLOWED_IMAGE_TYPES=image/jpeg,image/png,image/gif
MAX_IMAGE_SIZE=10485760
### 📡 API Endpoints
### Аутентификация
POST /api/register - регистрация пользователя

POST /api/login - получение JWT токена

GET /api/me - информация о текущем пользователе

### Работа с изображениями
POST /api/upload - загрузка изображения

GET /api/images/{id} - получение изображения по ID



### 🖼 Загрузка изображений
Базовая загрузка
```
curl -X POST http://localhost:8080/api/upload \
  -H "Authorization: Bearer <your_token>" \
  -F "file=@/path/to/image.png"
```
Загрузка с параметрами обработки
```
curl -X POST http://localhost:8080/api/upload \
  -H "Authorization: Bearer <your_token>" \
  -F "file=@/path/to/image.png" \
  -F "quality=80" \
  -F "x=800" \
  -F "y=600"
  ```
Получение изображения
```
curl -X GET http://localhost:8080/api/images/1 \
  -H "Authorization: Bearer <your_token>" \
  --output image.jpg
  ```
### 🔐 Аутентификация
Регистрация пользователя
```
curl -X POST http://localhost:8080/api/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "securepassword"
  }'
  ```
Получение токена
```
curl -X POST http://localhost:8080/api/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "securepassword"
  }'
  ```
Использование токена
Добавьте заголовок в запросы:

```
Authorization: Bearer <your_token>
```
### 🗄 Структура проекта
```
app/
├── main.py                 # Точка входа приложения
├── config.py              # Конфигурация приложения
├── database.py            # Настройка базы данных
├── models/                # Модели SQLAlchemy
│   ├── image.py
│   ├── user.py
│   └── log.py
├── repositories/          # Репозитории для работы с БД
│   ├── image_repo.py
│   ├── user_repo.py
│   └── log_repo.py
├── services/              # Бизнес-логика
│   ├── image_service.py
│   ├── auth_service.py
│   ├── log_service.py
│   └── minio_service.py
├── api/                   # API endpoints
│   ├── routes.py
│   ├── dependencies.py
│   └── middleware.py
├── schemas/               # Pydantic схемы
│   ├── image.py
│   ├── user.py
│   └── token.py
├── utils/                 # Вспомогательные утилиты
│   ├── image_processor.py
│   └── logging.py
└── migrations/            # Миграции базы данных
```
### 🐳 Docker
Сборка образа
```
docker compose build
```
Docker Compose
Запуск всего стека (приложение, PostgreSQL, MinIO):

```
docker compose up -d
```
Остановка:

```
docker-compose down
```
Просмотр логов:

```
docker-compose logs -f app
```
### 🔧 Разработка
Установка для разработки
Создайте виртуальное окружение:

```
python -m venv venv
source venv/bin/activate  # Linux/Mac)
# или
venv\Scripts\activate     # Windows
```
Установите зависимости:

```
pip install -r requirements.txt
```
Запустите сервисы через Docker Compose:

```
docker-compose up -d postgres minio
```
Запустите приложение:

```
python main.py
```
Создание миграций
```
alembic revision --autogenerate -m "Description of changes"
alembic upgrade head
```
Тестирование
```
pytest tests/
```
### 📊 Логирование
Приложение использует структурированное логирование в формате:

```
%(asctime)s,%(msecs)d: %(route)s: %(functionName)s: %(levelname)s: %(message)s
```