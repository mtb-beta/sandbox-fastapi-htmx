from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <html>
        <head>
            <title>FastAPI + HTMX Tutorial</title>
        </head>
        <body>
            <h1>Hello FastAPI with HTML!</h1>
            <p>これはHTMLレスポンスです。</p>
        </body>
    </html>
    """
