from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = "finance.db"

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                amount REAL,
                comment TEXT,
                type TEXT,
                timestamp DATETIME
            )
        """)

init_db()

class Entry(BaseModel):
    user_id: str
    amount: float
    comment: str
    type: str

@app.get("/")
async def read_index():
    # Проверяем самый простой путь
    if os.path.exists("money_webapp.html"):
        return FileResponse("money_webapp.html")
    return {"error": "money_webapp.html not found in root directory"}

@app.get("/balance/{user_id}")
async def get_balance(user_id: str):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT amount, type FROM entries WHERE user_id = ?", (user_id,))
        rows = cursor.fetchall()
        total = sum(amount if entry_type == 'income' else -amount for amount, entry_type in rows)
        return {"balance": total}

@app.get("/history/{user_id}")
async def get_history(user_id: str):
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM entries WHERE user_id = ? ORDER BY timestamp DESC", (user_id,))
        return [dict(row) for row in cursor.fetchall()]

@app.post("/add")
async def add_entry(entry: Entry):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO entries (user_id, amount, comment, type, timestamp) VALUES (?, ?, ?, ?, ?)",
            (entry.user_id, entry.amount, entry.comment, entry.type, datetime.now().isoformat())
        )
    return {"status": "success"}

@app.delete("/delete/{entry_id}")
async def delete_entry(entry_id: int):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("DELETE FROM entries WHERE id = ?", (entry_id,))
    return {"status": "deleted"}
