from fastapi import FastAPI, HTTPException
import uuid

app = FastAPI(title="TaskManager")

tasks = {}

@app.post("/tasks", status_code=201)
async def create_task(task: TaskCreate):
    task_id = str(uuid.uuid4())
    task_data = task.model_dump()
    task_data["id"] = task_id
    tasks[task_id] = task_data
    return task_data

@app.get("/tasks/{task_id}")
async def get_task(task_id: str):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks[task_id]