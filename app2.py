from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
import uuid

app = FastAPI(
    title="TaskManager API",
    description="API для управления задачами. Позволяет создавать и получать задачи с приоритетами.",
    version="1.0.0",
    contact={
        "name": "API Support",
        "email": "support@example.com",
    },
    license_info={
        "name": "MIT",
    }
)

tasks = {}

class TaskCreate(BaseModel):
    """
    Модель для создания новой задачи.
    """
    title: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Заголовок задачи. Должен содержать от 3 до 100 символов.",
        example="Разработать REST API"
    )
    description: Optional[str] = Field(
        None,
        description="Подробное описание задачи (необязательное поле).",
        example="Создать полноценное API для управления задачами с использованием FastAPI"
    )
    priority: int = Field(
        ...,
        ge=1,
        le=5,
        description="Приоритет задачи. Значение от 1 (низкий) до 5 (высокий).",
        example=3
    )

class TaskResponse(BaseModel):
    """
    Модель ответа с данными задачи.
    """
    id: str = Field(
        ...,
        description="Уникальный идентификатор задачи (UUID).",
        example="3fa85f64-5717-4562-b3fc-2c963f66afa6"
    )
    title: str = Field(
        ...,
        description="Заголовок задачи.",
        example="Разработать REST API"
    )
    description: Optional[str] = Field(
        None,
        description="Описание задачи.",
        example="Создать полноценное API для управления задачами"
    )
    priority: int = Field(
        ...,
        description="Приоритет задачи (1-5).",
        example=3
    )

@app.post(
    "/tasks",
    status_code=201,
    response_model=TaskResponse,
    tags=["Задачи"],
    summary="Создать новую задачу",
    description="Создает новую задачу с указанными заголовком, описанием и приоритетом. "
                "Возвращает созданную задачу с уникальным идентификатором."
)
async def create_task(task: TaskCreate):
    """
    Создание новой задачи.

    - **title**: Обязательное поле, от 3 до 100 символов
    - **description**: Необязательное поле
    - **priority**: Обязательное поле, от 1 до 5

    Возвращает созданную задачу с автоматически сгенерированным UUID.
    """
    task_id = str(uuid.uuid4())
    task_data = {
        "id": task_id,
        "title": task.title,
        "description": task.description,
        "priority": task.priority
    }
    tasks[task_id] = task_data
    return task_data

@app.get(
    "/tasks/{task_id}",
    response_model=TaskResponse,
    tags=["Задачи"],
    summary="Получить задачу по ID",
    description="Возвращает задачу по её уникальному идентификатору. "
                "Если задача не найдена, возвращает ошибку 404."
)
async def get_task(task_id: str):
    """
    Получение задачи по идентификатору.

    - **task_id**: UUID задачи

    Возвращает полные данные задачи.
    """
    if task_id not in tasks:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )
    return tasks[task_id]

# Добавляем информативные примеры для Swagger UI
@app.get(
    "/",
    tags=["Root"],
    summary="Корневой эндпоинт",
    description="Приветственное сообщение API.",
    include_in_schema=False
)
async def root():
    return {"message": "TaskManager API. Документация доступна по адресу /docs"}

# Настройка тегов для группировки эндпоинтов в Swagger
tags_metadata = [
    {
        "name": "Задачи",
        "description": "Операции с задачами: создание и получение.",
    }
]

app.openapi_tags = tags_metadata