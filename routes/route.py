from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient


client = MongoClient('mongodb://localhost:27017/')
conn = client.Test

notes = APIRouter()
templates = Jinja2Templates(directory="templates")

@notes.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    docs = conn.Test.find({})
    newDocs = []
    for doc in docs:
        newDocs.append({
            "id": str(doc["_id"]),
            "title": doc["title"],
            "desc": doc["desc"],
        })
    return templates.TemplateResponse("index.html", {"request": request, "newDocs": newDocs})

@notes.post("/")
async def create_item(request: Request, title: str = Form(...), desc: str = Form(...), important: bool = Form(False)):
    note = {
        "title": title,
        "desc": desc,
        "important": important
    }
    conn.Test.insert_one(note)
    return {"Success": True}
