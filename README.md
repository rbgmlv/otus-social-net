# Social Network API

Базовый скелет социальной сети на Python/Flask с PostgreSQL.

## Требования

- Docker и Docker Compose
- Или Python 3.13+ и PostgreSQL 15+

## Локальный запуск

### Вариант 1: Docker Compose (рекомендуется)

```bash
# Запуск всех сервисов
docker-compose up -d

# Приложение будет доступно на http://localhost:5000
```

### Вариант 2: Ручной запуск

1. Запустите PostgreSQL и создайте базу данных:

```bash
# Если PostgreSQL запущен локально
psql -U postgres -c "CREATE DATABASE social_network;"
psql -U postgres -d social_network -f init.sql
```

2. Установите uv (менеджер пакетов):

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

3. Установите зависимости:

```bash
uv sync
```

4. Настройте переменные окружения:

```bash
cp .env.example .env
# Отредактируйте .env при необходимости
```

5. Запустите приложение:

```bash
uv run python run.py
```

## API Endpoints

### POST /user/register

Регистрация нового пользователя.

**Request:**
```json
{
  "first_name": "Иван",
  "second_name": "Иванов",
  "birthdate": "1990-01-15",
  "gender": "male",
  "biography": "Люблю программирование",
  "city": "Москва",
  "password": "securepassword123"
}
```

**Response (200):**
```json
{
  "user_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

### POST /login

Авторизация пользователя.

**Request:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "password": "securepassword123"
}
```

**Response (200):**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### GET /user/get/{id}

Получение анкеты пользователя.

**Response (200):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "first_name": "Иван",
  "second_name": "Иванов",
  "birthdate": "1990-01-15",
  "gender": "male",
  "biography": "Люблю программирование",
  "city": "Москва"
}
```

## Примеры использования (curl)

```bash
# Регистрация
curl -X POST http://localhost:5000/user/register \
  -H "Content-Type: application/json" \
  -d '{"first_name":"Иван","second_name":"Иванов","birthdate":"1990-01-15","gender":"male","biography":"Программист","city":"Москва","password":"test123"}'

# Авторизация (подставьте user_id из предыдущего ответа)
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"id":"USER_ID_HERE","password":"test123"}'

# Получение анкеты
curl http://localhost:5000/user/get/USER_ID_HERE
```

## Архитектура

```
otus-project-01/
├── app/
│   ├── __init__.py          # Flask application factory
│   ├── db/
│   │   └── connection.py    # PostgreSQL connection (без ORM)
│   ├── models/
│   │   └── user.py          # Модель пользователя с SQL-запросами
│   ├── routes/
│   │   ├── auth.py          # Эндпойнт /login
│   │   └── user.py          # Эндпойнты /user/*
│   └── utils/
│       ├── response.py      # UserResponseModel для форматирования ответов
│       └── security.py      # bcrypt + JWT
├── config.py                 # Конфигурация
├── run.py                    # Точка входа
├── init.sql                  # Схема БД
├── docker-compose.yml        # Сервисы Docker
├── Dockerfile               # App container
├── pyproject.toml           # Зависимости (uv)
└── uv.lock                  # Lock-файл
```

## Особенности реализации

- Без ORM — все SQL-запросы написаны вручную с параметризацией
- Защита от SQL-инъекций — используются параметризованные запросы (плеймхолдеры %s )
- Безопасное хранение паролей — bcrypt для хеширования
- JWT токены для авторизации пользователей
- Менеджер пакетов uv
