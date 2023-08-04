from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from lib.api.types import Page, MetaTags, Data
from lib.model import query_vector_db

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates: Jinja2Templates = Jinja2Templates(directory="static/html")


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            data = await websocket.receive_text()
            # Function to process the query and generate a response
            response = query_vector_db(data)
            await websocket.send_text(f"AI Assistant: {response}")
        except WebSocketDisconnect:
            break


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    page = Page(
        request=request,
        title="AI Chatbot",
        slug="",
        notification=False,
        notification_message="",
        content="",
        breadcrumb=[],
        meta=MetaTags(
            product="AI Customer Chatbot Demo",
            title="AI Chatbot",
            description="AI Chatbot",
            type="Demo",
            url="",
            image="",

        ),
        data=Data(),
    )
    return templates.TemplateResponse("index.html", page.dict())
