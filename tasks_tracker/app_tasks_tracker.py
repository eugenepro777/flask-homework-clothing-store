from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import pandas as pd

app = FastAPI()
templates = Jinja2Templates(directory="./tasks_tracker/templates")

tasks = []


class Task(BaseModel):
    id: int
    title: str
    description: str
    status: bool = False


@app.get("/tasks", response_class=HTMLResponse)
async def read_tasks(request: Request):
    tasks_table = pd.DataFrame([vars(task) for task in tasks]).to_html()
    return templates.TemplateResponse("tasks.html", {"request": request, "tasks_table": tasks_table})


@app.get("/tasks/{task_id}", response_class=HTMLResponse)
async def read_task(request: Request, task_id: int):
    if task_id >= len(tasks):
        raise HTTPException(status_code=404, detail="Задача не найдена")
    task = pd.DataFrame([vars(t) for t in tasks if t.id == task_id]).to_html()
    return templates.TemplateResponse("tasks.html", {"request": Request, "task": task})


@app.post("/tasks", response_model=Task)
async def create_task(task: Task):
    task_id = len(tasks) + 1
    task.id = task_id
    tasks.append(task)
    return task