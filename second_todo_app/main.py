import uuid
from datetime import datetime
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="second_todo_app/templates")

# Todoを格納する辞書に変更
todos = {}


# 初期データを追加
def init_todos():
    for title in ["FastAPIを学ぶ", "HTMXを理解する", "Todoアプリを作る"]:
        todo_id = str(uuid.uuid4())
        todos[todo_id] = {"id": todo_id, "title": title, "completed": False}


init_todos()


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "title": "My Todo App", "todos": todos.values()},
    )


@app.post("/todos", response_class=HTMLResponse)
async def create_todo(request: Request, title: str = Form(...)):
    todo_id = str(uuid.uuid4())
    todo = {"id": todo_id, "title": title, "completed": False}
    todos[todo_id] = todo

    # 新しいTodoアイテムのHTMLだけを返す
    return templates.TemplateResponse(
        "partials/todo_item.html", {"request": request, "todo": todo}
    )
