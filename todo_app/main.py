from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import Optional
from datetime import datetime
import uuid

app = FastAPI()
templates = Jinja2Templates(directory="todo_app/templates")

# メモリ内でTodoを管理（本番環境ではデータベースを使用）
todos = {}


class Todo:
    def __init__(self, title: str, completed: bool = False):
        self.id = str(uuid.uuid4())
        self.title = title
        self.completed = completed
        self.created_at = datetime.now()


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """メインページの表示"""
    return templates.TemplateResponse(
        "index.html", {"request": request, "todos": todos.values()}
    )


@app.post("/todos", response_class=HTMLResponse)
async def create_todo(request: Request, title: str = Form(...)):
    """新しいTodoの作成"""
    todo = Todo(title=title)
    todos[todo.id] = todo

    # HTMXレスポンス: 新しいTodoアイテムのHTMLのみを返す
    return templates.TemplateResponse(
        "partials/todo_item.html", {"request": request, "todo": todo}
    )


@app.delete("/todos/{todo_id}", response_class=HTMLResponse)
async def delete_todo(todo_id: str):
    """Todoの削除"""
    if todo_id in todos:
        del todos[todo_id]
    # HTMXは200-299のステータスコードで要素を削除
    return ""


@app.put("/todos/{todo_id}/toggle", response_class=HTMLResponse)
async def toggle_todo(request: Request, todo_id: str):
    """Todoの完了状態を切り替え"""
    if todo_id in todos:
        todos[todo_id].completed = not todos[todo_id].completed
        return templates.TemplateResponse(
            "partials/todo_item.html", {"request": request, "todo": todos[todo_id]}
        )
    return ""


@app.get("/todos/count")
async def get_todo_count():
    """未完了のTodo数を取得"""
    count = sum(1 for todo in todos.values() if not todo.completed)
    return HTMLResponse(content=f"{count} 件のタスク")
