from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os
from pymongo import MongoClient

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Получаем ссылку на БД из настроек Render
# В Render мы добавим переменную окружения MONGO_URI
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client.finance_db
entries_collection = db.entries

class Entry(BaseModel):
    user_id: str
    amount: float
    comment: str
    type: str

@app.get("/")
async def read_index():
    if os.path.exists("money_webapp.html"):
        return FileResponse("money_webapp.html")
    return {"error": "money_webapp.html not found"}

@app.get("/balance/{user_id}")
async def get_balance(user_id: str):
    cursor = entries_collection.find({"user_id": user_id})
    total = 0
    for entry in cursor:
        total += entry['amount'] if entry['type'] == 'income' else -entry['amount']
    return {"balance": total}

@app.get("/history/{user_id}")
async def get_history(user_id: str):
    # Получаем записи, заменяя _id MongoDB на обычный id для фронтенда
    cursor = entries_collection.find({"user_id": user_id}).sort("timestamp", -1)
    history = []
    for entry in cursor:
        entry['_id'] = str(entry['_id'])
        history.append(entry)
    return history

@app.post("/add")
async def add_entry(entry: Entry):
    document = {
        "user_id": entry.user_id,
        "amount": entry.amount,
        "comment": entry.comment,
        "type": entry.type,
        "timestamp": datetime.now()
    }
    entries_collection.insert_one(document)
    return {"status": "success"}

@app.delete("/delete/{entry_id}")
async def delete_entry(entry_id: str):
    from bson.objectid import ObjectId
    entries_collection.delete_one({"_id": ObjectId(entry_id)})
    return {"status": "deleted"}
