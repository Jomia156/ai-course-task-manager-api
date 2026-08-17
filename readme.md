# TaskManager API

Простое REST API для управления задачами, построенное на FastAPI.

## Содержание

1. [Быстрый старт](#1-быстрый-старт)
2. [API Эндпоинты](#2-api-эндпоинты)
3. [Модели данных](#3-модели-данных)
4. [Примеры использования](#4-примеры-использования)
5. [Коды ответов](#5-коды-ответов)
6. [Установка и запуск](#6-установка-и-запуск)
7. [Хранение данных](#7-хранение-данных)
8. [Лицензия](#8-лицензия)

## 1. Быстрый старт

Установка зависимостей:

```bash
pip install fastapi uvicorn
```

Запуск сервера:

```bash
uvicorn main:app --reload
```

Сервер запустится на http://localhost:8000

Документация API:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 2. API Эндпоинты

### 2.1. POST /tasks - Создание задачи

Создает новую задачу в системе.

Статус ответа: `201 Created`

Тело запроса (JSON):

| Поле        | Тип     | Обязат. | Ограничения    | Описание         |
|-------------|---------|---------|----------------|------------------|
| title       | string  | Да      | 3-100 символов | Заголовок задачи |
| description | string  | Нет     | -              | Описание задачи  |
| priority    | integer | Да      | 1-5            | Приоритет задачи |

Пример запроса:

```http
POST /tasks HTTP/1.1
Host: localhost:8000
Content-Type: application/json

{
    "title": "Разработать REST API",
    "description": "Создать API для управления задачами",
    "priority": 3
}
```

Успешный ответ (201 Created):

```json
{
    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "title": "Разработать REST API",
    "description": "Создать API для управления задачами",
    "priority": 3
}
```

Ошибка валидации (422 Unprocessable Entity):

```json
{
    "detail": [
        {
            "loc": ["body", "title"],
            "msg": "ensure this value has at least 3 characters",
            "type": "value_error.any_str.min_length",
            "ctx": {"limit_value": 3}
        },
        {
            "loc": ["body", "priority"],
            "msg": "ensure this value is less than or equal to 5",
            "type": "value_error.number.not_le",
            "ctx": {"limit_value": 5}
        }
    ]
}
```

### 2.2. GET /tasks/{task_id} - Получение задачи

Возвращает задачу по её идентификатору.

Статус ответа: `200 OK`

Параметры пути:

| Параметр | Тип    | Обязат. | Описание   |
|----------|--------|---------|------------|
| task_id  | string | Да      | UUID задачи |

Пример запроса:

```http
GET /tasks/3fa85f64-5717-4562-b3fc-2c963f66afa6 HTTP/1.1
Host: localhost:8000
```

Успешный ответ (200 OK):

```json
{
    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "title": "Разработать REST API",
    "description": "Создать API для управления задачами",
    "priority": 3
}
```

Ошибка - задача не найдена (404 Not Found):

```json
{
    "detail": "Task not found"
}
```

## 3. Модели данных

**TaskCreate** (Запрос на создание):

```json
{
    "title": "string (3-100 символов, обязательное)",
    "description": "string (опционально)",
    "priority": "integer (1-5, обязательное)"
}
```

**TaskResponse** (Ответ с данными задачи):

```json
{
    "id": "string (UUID)",
    "title": "string",
    "description": "string или null",
    "priority": "integer"
}
```

## 4. Примеры использования

### 4.1. cURL

Создание задачи:

```bash
curl -X POST "http://localhost:8000/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Тестовая задача",
    "description": "Описание задачи",
    "priority": 2
  }'
```

Получение задачи:

```bash
curl -X GET "http://localhost:8000/tasks/3fa85f64-5717-4562-b3fc-2c963f66afa6"
```

### 4.2. Python (requests)

```python
import requests

# Создание задачи
response = requests.post(
    "http://localhost:8000/tasks",
    json={
        "title": "Написать документацию",
        "description": "Создать README.md",
        "priority": 4
    }
)

if response.status_code == 201:
    task = response.json()
    task_id = task["id"]
    print(f"Задача создана с ID: {task_id}")
else:
    print(f"Ошибка: {response.status_code}")

# Получение задачи
response = requests.get(f"http://localhost:8000/tasks/{task_id}")

if response.status_code == 200:
    task = response.json()
    print(f"Задача: {task['title']}")
    print(f"Приоритет: {task['priority']}")
else:
    print("Задача не найдена")
```

### 4.3. JavaScript (fetch)

```javascript
// Создание задачи
const createTask = async () => {
    const response = await fetch('http://localhost:8000/tasks', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            title: 'Тестовая задача',
            description: 'Описание',
            priority: 3
        })
    });
    
    const data = await response.json();
    console.log('Создана задача:', data);
};

// Получение задачи
const getTask = async (taskId) => {
    const response = await fetch(`http://localhost:8000/tasks/${taskId}`);
    
    if (response.ok) {
        const task = await response.json();
        console.log('Задача:', task);
    } else {
        console.log('Задача не найдена');
    }
};
```

## 5. Коды ответов

| Код | Название             | Описание                          |
|-----|----------------------|-----------------------------------|
| 200 | OK                   | Запрос успешно выполнен           |
| 201 | Created              | Задача успешно создана            |
| 404 | Not Found            | Задача с указанным ID не найдена  |
| 422 | Unprocessable Entity | Ошибка валидации данных           |

## 6. Установка и запуск

Требования:
- Python 3.7+
- pip

Установка:

```bash
pip install fastapi uvicorn
```

Запуск в режиме разработки (с автоперезагрузкой):

```bash
uvicorn main:app --reload
```

Запуск в продакшн режиме:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## 7. Хранение данных

Приложение использует временное хранение в памяти (словарь Python).

> **ВНИМАНИЕ:** Все данные теряются при перезапуске сервера.

Для постоянного хранения рекомендуется использовать:
- PostgreSQL
- SQLite
- MongoDB
- Другие базы данных

## 8. Лицензия

MIT License

---

Документация создана для TaskManager API v1.0.0