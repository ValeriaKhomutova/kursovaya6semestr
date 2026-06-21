# Articles Platform

Backend-платформа для публикации статей, отзывов и управления пользователями, реализованная на Django + Django REST Framework с Docker-инфраструктурой, PostgreSQL и MinIO.

---

# О проекте

Проект предоставляет:

* REST API для работы со статьями и отзывами
* регистрацию и аутентификацию пользователей
* JWT authentication
* базовый frontend через Django templates
* хранение медиафайлов через MinIO (S3-compatible storage)
* production-ready Docker окружение
* запуск через Docker Compose
* pytest тестирование

---

# Технологии

* Python 3.12
* Django
* Django REST Framework
* Gunicorn
* PostgreSQL
* MinIO
* WhiteNoise
* Pytest
* Docker & Docker Compose
* HTML / CSS / JavaScript

---

# Архитектура проекта

Проект построен с использованием принципов **12-Factor App**:

* конфигурация через environment variables
* stateless application
* external backing services
* isolated dependencies
* production-ready process model
* Dockerized runtime environment

---

# Структура проекта

```text
articles/
│
├── articleplatform/
│   ├── article_module/        # статьи
│   ├── reviews/               # отзывы
│   ├── users/                 # пользователи
│   ├── templates/             # HTML шаблоны
│   ├── static/                # CSS / JS
│   ├── articleplatform/       # настройки Django
|   ├── Dockerfile
│   ├── manage.py
│   └── pytest.ini
│
├── docker-compose.yml
├── .env.example
├── .dockerignore
├── requirements.txt
└── README.md
```

---

# Используемые сервисы

## PostgreSQL

Используется как основная база данных.

## MinIO

Используется как S3-compatible object storage для:

* изображений
* пользовательских файлов
* media uploads

## WhiteNoise

Используется для раздачи static файлов в production.

---

# Environment Variables

Проект использует `.env` файл.

Создайте `.env` на основе `.env.example`.

## Пример

```env
DEBUG=False

SECRET_KEY=your_secret_key

ALLOWED_HOSTS=localhost,127.0.0.1

DB_USER=postgres
DB_NAME=articles_db
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432

MINIO_ROOT_USER=minio
MINIO_ROOT_PASSWORD=minio123

AWS_ACCESS_KEY_ID=minio
AWS_SECRET_ACCESS_KEY=minio123
AWS_STORAGE_BUCKET_NAME=article-platform-files
AWS_S3_ENDPOINT_URL=http://minio:9000
AWS_S3_REGION_NAME=us-east-1

CORS_ALLOW_ALL_ORIGINS=False
```

---

# Запуск через Docker Compose

## 1. Клонирование репозитория

```bash
git clone https://github.com/ValeriaKhomutova/articles.git

cd articles
```

---

## 2. Создание .env

```bash
cp .env.example .env
```

Заполните переменные окружения.

---

## 3. Запуск контейнеров

```bash
docker compose up --build
```

---

# Сервисы

После запуска будут доступны:

| Сервис        | URL                   |
| ------------- | --------------------- |
| Django        | http://localhost:8000 |
| PostgreSQL    | localhost:5432        |
| MinIO API     | http://localhost:9000 |
| MinIO Console | http://localhost:9001 |

---

# Docker Architecture

Проект запускает:

* Django application
* Gunicorn WSGI server
* PostgreSQL database
* MinIO object storage

Все сервисы работают внутри Docker Compose network.

---

# Production Features

Проект включает:

* Gunicorn workers
* healthcheck для PostgreSQL
* restart policies
* non-root Docker user
* isolated container networking
* environment-based configuration
* WhiteNoise static serving
* persistent Docker volumes

---

# Static и Media Files

## Static files

Static файлы обслуживаются через WhiteNoise:

```python
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

## Media files

Media файлы хранятся в MinIO через:

```python
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Storage'
```

---

# Локальный запуск без Docker

## 1. Создание виртуального окружения

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

---

## 2. Установка зависимостей

```bash
pip install -r requirements.txt
```

---

## 3. Переход в проект

```bash
cd articleplatform
```

---

## 4. Миграции

```bash
python manage.py migrate
```

---

## 5. Запуск сервера

```bash
python manage.py runserver
```

---

# Тестирование

```bash
pytest
```

---

# Основные Django приложения

| Приложение     | Назначение                    |
| -------------- | ----------------------------- |
| users          | пользователи и authentication |
| article_module | статьи                        |
| reviews        | отзывы                        |

---

# Автор

Valeria Khomutova
