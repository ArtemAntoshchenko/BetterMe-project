# BetterMe

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)](https://redis.io/)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![Jinja](https://img.shields.io/badge/jinja-white.svg?style=for-the-badge&logo=jinja&logoColor=black)](https://jinja.palletsprojects.com/)

Учебный проект по созданию веб-сайта для закрепления полезных привычек **BetterMe**. Это мой первый большой REST API проект, построенный на современном асинхронном фреймворке FastAPI. Проект представляет собой полноценный сайт с возможностью регистрации, ведения списка привычек, отслеживания прогресса и получения достижений.

## Ключевые особенности

- **🔐 Безопасность:** Аутентификация на основе JWT-токенов и надежное хеширование паролей с помощью bcrypt.
- **⚡ Производительность:** Полностью асинхронное ядро приложения и кеширование данных в Redis для быстрого отклика.
- **📝 Работа с данными:** Валидация и сериализация данных осуществляется через Pydantic-схемы.
- **📚 Документация:** Автоматически сгенерированная документация Swagger (OpenAPI) для всех эндпоинтов API.
- **🌦️ Интеграция с внешним API:** Асинхронное подключение к погодному API с помощью библиотеки `aiohttp`.
- **🐳 Контейнеризация:** Проект полностью упакован в Docker-контейнеры для простого и быстрого развертывания.

## Технологический стек

- **Бэкенд:**
  - [FastAPI](https://fastapi.tiangolo.com/) — современный, быстрый веб-фреймворк.
  - [SQLAlchemy 2.0](https://www.sqlalchemy.org/) — полноценная ORM с асинхронной поддержкой.
  - [Pydantic v2](https://docs.pydantic.dev/) — валидация данных на основе аннотаций типов.
  - [Redis](https://redis.io/) — быстрое in-memory хранилище для кеширования.
  - [Alembic](https://alembic.sqlalchemy.org/) — инструмент для управления миграциями базы данных.
- **Фронтенд:**
  - [Jinja2](https://jinja.palletsprojects.com/) — шаблонизатор для генерации HTML-страниц.
- **База данных:**
  - [asyncpg (PostgreSQL)](https://github.com/MagicStack/asyncpg) — асинхронный драйвер для PostgreSQL.
- **Инфраструктура:**
  - [Docker](https://www.docker.com/) — контейнеризация.

## Запуск проекта

Следуйте одному из двух вариантов, чтобы запустить проект.

### Вариант 1: Локальная установка

**Требования:** Установленные PostgreSQL и Redis на вашем устройстве.

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

## Структура проекта

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
├── .env                  # Переменные окружения
├── .gitignore
├── alembic.ini
├── docker-compose.yml    # Конфигурация Docker Compose
├── Dockerfile            # Инструкция для сборки Docker-образа
├── LICENSE.md            # Лицензия MIT
├── README.md             # Документация проекта
└── requirements.txt      # Зависимости проекта

<img width="248" height="674" alt="Структура проекта" src="https://github.com/user-attachments/assets/36a07b3a-02fc-4574-8f43-4293ac8d6839" />

## Лицензия

Проект распространяется под лицензией MIT. Подробнее в файле LICENSE.md.

## Контакты

**Автор:** Антощенко Артём

**Email:** fgd19611@yandex.ru

**GitHub:** ArtemAntoshchenko