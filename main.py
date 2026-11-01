from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os
from pymongo import MongoClient
from bson import ObjectId

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение к MongoDB Atlas
MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    print("ОШИБКА: Переменная MONGO_URI не найдена в настройках Render!")

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
    # Ищем все записи пользователя
    cursor = entries_collection.find({"user_id": user_id})
    total = 0.0
    for entry in cursor:
        amount = entry.get('amount', 0)
        entry_type = entry.get('type', 'expense')
        total += amount if entry_type == 'income' else -amount
    return {"balance": total}

@app.get("/history/{user_id}")
async def get_history(user_id: str):
    # Получаем записи, сортируем по дате (сначала новые)
    cursor = entries_collection.find({"user_id": user_id}).sort("timestamp", -1)

    history = []
    for entry in cursor:
        # ВАЖНО: Превращаем _id (ObjectId) в обычную строку id, чтобы фронтенд ее видел
        history.append({
            "id": str(entry["_id"]),
            "amount": entry.get("amount", 0),
            "comment": entry.get("comment", ""),
            "type": entry.get("type", "expense"),
            "timestamp": entry.get("timestamp", datetime.now()).isoformat() if isinstance(entry.get("timestamp"), datetime) else entry.get("timestamp", datetime.now().isoformat())
        })
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
    try:
        entries_collection.delete_one({"_id": ObjectId(entry_id)})
        return {"status": "deleted"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)
