﻿# Cистема управления библиотекой на FastAPI

Этот проект представляет собой готовое приложение для разработки масштабируемого веб-приложений на основе **FastAPI** 
для управления библиотекой книг. Приложение позволяет добавлять, удалять, искать и отображать книги. 
Проект включает модульную архитектуру, поддерживает гибкое логирование с **loguru**, и взаимодействие с базой данных 
через **SQLAlchemy** с асинхронной поддержкой. Система миграций **Alembic** упрощает работу со схемой базы данных.

## Стек технологий

- **Веб-фреймворк**: FastAPI
- **ORM**: SQLAlchemy
- **База данных**: PostgeSQL
- **Система миграций**: Alembic

## Зависимости проекта

- `fastapi[all]==0.115.0` - высокопроизводительный веб-фреймворк
- `pydantic==2.9.2` - валидация данных
- `uvicorn==0.31.0` - ASGI-сервер
- `jinja2==3.1.4` - шаблонизатор
- `SQLAlchemy==2.0.35` - ORM для работы с базами данных
- `alembic==1.13.3` - управление миграциями базы данных
- `loguru==0.7.2` - красивое и удобное логирование
- `pytest~=8.3.3` - фреймворк для тестирования
- `aiohttp~=3.11.9` - ассинхронные запросы
- `pytest-asyncio~=0.24.0` - ассинхронный плагин pytest


### Основные модули

- **app/author** - Модуль для CRUD операций с авторами:
    - **dao.py**: Объект доступа к данным для работы с авторами
    - **models.py**: Модели данных для авторов
    - **router.py**: Маршрутизация запросов, связанных с CRUD  операциями
    - **schemas.py**: Схемы Pydantic для валидации запросов и ответов
- **app/book** - Модуль для CRUD операций с книгами:
    - **dao.py**: Объект доступа к данным для работы с книгами
    - **models.py**: Модели данных для книг
    - **router.py**: Маршрутизация запросов, связанных с CRUD  операциями
    - **schemas.py**: Схемы Pydantic для валидации запросов и ответов
- **app/borrow** - Модуль для CRUD операций с записями о выдаче книги:
    - **dao.py**: Объект доступа к данным для работы с записями о выдаче книги
    - **models.py**: Модели данных для записей о выдаче книг
    - **router.py**: Маршрутизация запросов, связанных с CRUD  операциями
    - **schemas.py**: Схемы Pydantic для валидации запросов и ответов
- **app/users** - Модуль для CRUD операций с записями о выдаче книги:
    - **dao.py**: Объект доступа к данным для работы с пользователями
    - **models.py**: Модели данных для пользователей
    - **router.py**: Маршрутизация запросов, связанных с CRUD  операциями
    - **schemas.py**: Схемы Pydantic для валидации запросов и ответов
    - **auth.py**: Аутентификация и авторизация пользователей


- **app/dao** - Базовый DAO для доступа к данным приложения.
    - **base.py**: Общие методы CRUD для работы с БД

- **app/migration** - Управление миграциями базы данных с помощью Alembic:
    - **versions/**: Файлы миграций
    - **env.py**: Конфигурация среды Alembic


- **config.py** - Файл конфигурации с параметрами приложения, загружаемыми из `.env`.

- **database.py** - Управление подключением и сессиями SQLAlchemy.

- **main.py** - Запуск приложения, настройка маршрутов и начальных параметров.


## Запуск приложения

1. Клонируйте репозиторий:

   ```bash
   git clone https://github.com/CapitanGrant/LibrarybookFastAPI_test
   ```

2. Установите зависимости:

   ```bash
   pip install -r requirements.txt
   ```

3. Создайте и настройте `.env` файл:

   ```env
   SECRET_KEY="ваш_секретный_ключ"
   ALGORITHM=HS256
   DB_USER=postgres_user
   DB_PASSWORD=postgres_password
   DB_HOST=localhost
   DB_PORT=5433
   DB_NAME=postgres_db
   ```
4. Запустите docker контейнер c PostgreSQL:

   ```bash
   docker compose up -d
   ```

5. Запустите приложение с Uvicorn:

   ```bash
   uvicorn app.main:app --reload
   ```

## Миграции базы данных

1. Инициализируйте Alembic:

   ```bash
   cd app
   alembic init -t async migration
   ```

   Затем переместите `alembic.ini` в корень проекта.

2. В `alembic.ini` установите `script_location` как `app/migration`.

3. Создайте миграцию:

   ```bash
   alembic revision --autogenerate -m "Initial migration"
   ```

4. Примените миграции:

   ```bash
   alembic upgrade head
   ```
5. Для запуска тестов используйте файл:
    ```bash
   tests/tests.py
   ```
6. Запустите приложение FastAPI app/main.py:
    ```bash
   uvicorn app.main:app --reload
   ```
7. Для чтения документации перейдите по ссылке
   ```браузер
   http://127.0.0.1:8000/docs#/
   ```
