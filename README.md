# BetterMe

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)](https://redis.io/)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![Jinja](https://img.shields.io/badge/jinja-white.svg?style=for-the-badge&logo=jinja&logoColor=black)](https://jinja.palletsprojects.com/)
[![Gunicorn](https://img.shields.io/badge/gunicorn-%298729.svg?style=for-the-badge&logo=gunicorn&logoColor=white)](https://gunicorn.org/)
[![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)](https://nginx.org/)
[![Pytest](https://img.shields.io/badge/pytest-%23ffffff.svg?style=for-the-badge&logo=pytest&logoColor=0a0a0a)](https://docs.pytest.org/)

Учебный проект по созданию веб-сайта для закрепления полезных привычек **BetterMe**. Это мой первый большой REST API проект, построенный на современном асинхронном фреймворке FastAPI. Проект представляет собой полноценный сайт с возможностью регистрации, ведения списка привычек, отслеживания прогресса и получения достижений.

## Ключевые особенности

- **🔐 Безопасность:** Аутентификация на основе JWT-токенов и надежное хеширование паролей с помощью bcrypt.
- **⚡ Производительность:** Полностью асинхронное ядро приложения и многоуровневое кэширование (Redis + Nginx + браузер) для быстрого отклика.
- **📝 Работа с данными:** Валидация и сериализация данных осуществляется через Pydantic-схемы.
- **📚 Документация:** Автоматически сгенерированная документация Swagger (OpenAPI) для всех эндпоинтов API.
- **🌦️ Интеграция с внешним API:** Асинхронное подключение к погодному API с помощью библиотеки `aiohttp`.
- **🧪 Тестирование:** Частичное покрытие тестами ключевых компонентов: unit и интеграционные тесты для проверки взаимодействия с БД, e2e-тесты для проверки пользовательского сценария регистрации на сайте.
- **🐳 Контейнеризация:** Проект полностью упакован в Docker-контейнеры для простого и быстрого развертывания.

## Технологический стек

- **Бэкенд:**
  - [FastAPI](https://fastapi.tiangolo.com/) — современный, быстрый веб-фреймворк.
  - [SQLAlchemy 2.0](https://www.sqlalchemy.org/) — полноценная ORM с асинхронной поддержкой.
  - [Pydantic v2](https://docs.pydantic.dev/) — валидация данных на основе аннотаций типов.
  - [Redis](https://redis.io/) — быстрое in-memory хранилище для кеширования.
  - [Alembic](https://alembic.sqlalchemy.org/) — инструмент для управления миграциями базы данных.
- **Инфраструктура и DevOps**
   - [Nginx](https://nginx.org/) — reverse proxy, раздача статики, балансировка нагрузки, WebSocket прокси.
   - [Gunicorn](https://gunicorn.org/) + Uvicorn — ASGI сервер для production окружения.
   - [Docker](https://www.docker.com/) — контейнеризация всего стека.
- **Фронтенд:**
  - [Jinja2](https://jinja.palletsprojects.com/) — шаблонизатор для генерации HTML-страниц.
- **База данных:**
  - [asyncpg (PostgreSQL)](https://github.com/MagicStack/asyncpg) — асинхронный драйвер для PostgreSQL.
- **Тестирование:**
  - [Pytest](https://docs.pytest.org/) — основной фреймворк для написания тестов.
  - [pytest-asyncio](https://pytest-asyncio.readthedocs.io/) — поддержка асинхронных тестов.
  - [httpx](https://www.python-httpx.org/) — асинхронный HTTP клиент для тестирования API.
  - [pytest-env](https://pypi.org/project/pytest-env/) — управление переменными окружения в тестах.

## Запуск проекта

Следуйте одному из двух вариантов, чтобы запустить проект.

### Вариант 1: Локальная установка

**Требования:** Установленные PostgreSQL, Redis и Nginx на вашем устройстве.

1. **Клонирование репозитория:**
   git clone --branch main --single-branch https://github.com/ArtemAntoshchenko/BetterMe-project.git

2. **Создание виртуального окружения:**
   python -m venv venv
   
   **Для Linux/macOS:**
   source venv/bin/activate
   
   **Для Windows:**
   venv\Scripts\activate

3. **Установка зависимостей:**
   pip install -r requirements.txt

4. **Настройка переменных окружения:**
   
   Отредактируйте файл `.env` с учётом своих данных:

5. **Применение миграций:**
   alembic upgrade head

6. **Запуск сервера:**
   uvicorn backend.main:app --reload --port 8000

7. **Запуск Nginx (в отдельном терминале):**
   **Для Linux/macOS:**
   sudo systemctl start nginx
   
   **Для Windows:**
   cd C:\nginx
   start nginx

### Вариант 2: Запуск с Docker

**Требования:** Установленные Docker.

1. **Клонирование репозитория:**
   git clone --branch redis --single-branch https://github.com/ArtemAntoshchenko/BetterMe-project.git
   cd BetterMe-project

2. **Создание и запуск контейнера:**
   docker-compose up --build

3. **Доступ к сайту:**
   
   Откройте браузер и перейдите по адресу:
   http://localhost:8000

## Документация API

Структура проекта позволяет легко перемещаться по сайту через кнопки продвижения до регистрации, и через навигационное меню после регистрации и входа под своей учётной записью.

### Доступные эндпоинты 

- http://127.0.0.1:8000 - приветственная страница 
- http://127.0.0.1:8000/auth/registration - страница регистрации
- http://127.0.0.1:8000/docs - Swagger UI (документация API)

### Доступные эндпоинты (через Nginx)

- http://127.0.0.1:8080 - приветственная страница 
- http://127.0.0.1:8080/auth/registration - страница регистрации
- http://127.0.0.1:8080/docs - Swagger UI (документация API)

## Структура проекта

```
BetterMe/
├── alembic/              # Миграции базы данных
├── backend/
│   ├── core/             # Конфигурация, зависимости, безопасность
│   ├── DAO/              # data accesse objects
│   ├── db/               # SQLAlchemy модели
│   ├── routers/          # Роутеры и эндпоинты приложения
│   ├── schemas/          # Pydantic схемы
│   └── main.py           # Точка входа в приложение
├── frontend/
│   ├── static/           # CSS, JS, изображения
│   └── templates/        # HTML шаблоны
├── tests/
│   ├── e2e/              # тесты пользовательских сценариев
│   ├── integration/      # интеграционные тесты
│   └── unit/             # unit тесты
├── deploy/               # Конфигурации для production
│   ├── nginx/
│   │   └── betterme.conf # Полная конфигурация Nginx
├── .env                  # Переменные окружения
├── .gitignore
├── alembic.ini
├── docker-compose.yml    # Конфигурация Docker Compose
├── Dockerfile            # Инструкция для сборки Docker-образа
├── LICENSE.md            # Лицензия MIT
├── README.md             # Документация проекта
└── requirements.txt      # Зависимости проекта
```

<img width="350" height="872" alt="image" src="https://github.com/user-attachments/assets/6211521e-bd60-4007-89b2-bd8a7f2a3270" />

## Лицензия

Проект распространяется под лицензией MIT. Подробнее в файле LICENSE.md.

## Контакты

**Автор:** Антощенко Артём

**Email:** fgd19611@yandex.ru

**GitHub:** ArtemAntoshchenko
