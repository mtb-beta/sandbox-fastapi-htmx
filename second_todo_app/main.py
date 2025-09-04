from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime

app = FastAPI()
templates = Jinja2Templates(directory="second_todo_app/templates")

# Todoを格納するリスト（仮のデータ）
todos = [
    {"id": 1, "title": "FastAPIを学ぶ", "completed": False},
    {"id": 2, "title": "HTMXを理解する", "completed": False},
    {"id": 3, "title": "Todoアプリを作る", "completed": True},
]


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(
        "index.html", {"request": request, "title": "My Todo App", "todos": todos}
    )
