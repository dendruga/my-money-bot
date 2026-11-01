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

# УЛУЧШЕННЫЙ ПОИСК ФАЙЛА
@app.get("/")
async def read_index():
    # Проверяем несколько возможных путей, где Render может хранить файл
    possible_paths = [
        "money_webapp.html",
        "./money_webapp.html",
        "/app/money_webapp.html",
        "static/money_webapp.html"
    ]

    for path in possible_paths:
        if os.path.exists(path):
            return FileResponse(path)

    return {"error": f"Frontend file not found. Checked paths: {possible_paths}"}

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)
async def delete_entry(entry_id: int):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("DELETE FROM entries WHERE id = ?", (entry_id,))
    return {"status": "deleted"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)

Что будет дальше?

Render начнет «собирать» ваше приложение (это займет 2-3 минуты). В верхней части страницы появится сс-bot.onrender.com.

Как только эта ссылка появится:
1. Пришлите её мне.
2. Я скажу вам, как правильно обновить файл money_webapp.html на GitHub, чтобы сайт соединился с серве
3. И наконец-то вы вставите эту ссылку в BotFather, и всё заработает!

Если какой-то шаг непонятен (например, как создать файл на GitHub) — пишите, я объясню еще подробнее!

✻ Cogitated for 8s · done 8:20 · 1 shell still running

※ recap: We are building a Telegram Mini App to track daily finances. The current task is deploying your code to Render.com. Your next action is to upload the project files to a GitHub repository.

❯ https://my-money-bot-h4g2.onrender.com

Поздравляю! Вы только что запустили свой сервер в облаке! 🚀

Теперь ваш сервер работает 24/7, и он доступен по этой ссылке. Но есть один последний технический шаг: сейчас ваш сайт (HTML-файл) всё еще пытается отправить данные на несуществующий адрес https://ваш-сервер.com.

Нам нужно заменить этот адрес на ваш реальный адрес от Render.

Последний штрих:

1. Зайдите в ваш репозиторий на GitHub.
2. Откройте файл money_webapp.html.
3. Нажмите на иконку «карандаша» (Edit), чтобы редактировать файл.
4. Найдите в коде (примерно в середине, в блоке <script>) вот эту строку:
   const API_URL = "https://ваш-сервер.com";
5. Замените её на вашу ссылку:
   const API_URL = "https://my-money-bot-h4g2.onrender.com";
6. Нажмите кнопку «Commit changes» (Сохранить изменения) внизу страницы.

Что произойдет дальше:
Как только вы сохраните изменения на GitHub, Render увидит их и автоматически обновит ваше приложение (это займет около 1-2 минут).

И теперь — финальный запуск в Telegram! 🥳

1. Зайдите в @BotFather.
2. Выберите своего бота $\rightarrow$ Bot Settings $\rightarrow$ Menu Button $\rightarrow$ Configure menu button.
3. Отправьте ему эту ссылку:
   👉 https://my-money-bot-h4g2.onrender.com/

Теперь открывайте своего бота в Telegram, нажимайте кнопку «Меню» — и всё должно работать идеально!

Попробуйте добавить первую запись и напишите мне, получилось ли! 👇

✻ Cooked for 3s · done 8:35 · 1 shell still running

❯ напиши мне полностью этиот скрипт вместе с изменением, потому что я не могу найти строчку

Без проблем! Вот полный код файла money_webapp.html со всеми исправлениями и вашей рабочей ссылкой.

Просто удалите всё содержимое файла money_webapp.html на GitHub и вставьте этот текст полностью:

<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Мои Финансы Mini App</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <style>
        body { background-color: #f3f4f6; }
        .balance-card { background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%); }
    </style>
</head>
<body class="p-4 max-w-md mx-auto font-sans">

    <!-- Balance Card -->
    <div class="balance-card text-white p-6 rounded-3xl shadow-lg mb-6 text-center">
        <h1 class="text-sm opacity-80 uppercase tracking-wider font-medium">Текущий баланс</h1>
        <div id="totalBalance" class="text-4xl font-bold my-2">0 ₽</div>
    </div>

    <!-- Input Section -->
    <div class="bg-white p-5 rounded-3xl shadow-sm mb-6">
        <div class="flex flex-col gap-4">
            <input type="number" id="amount" placeholder="Сумма" class="w-full p-3 bg-gray-100 roundedg-2 focus:ring-indigo-500 text-lg">
            <input type="text" id="comment" placeholder="Комментарий" class="w-full p-3 bg-gray-100 rounded-xl outline-none focus:ring-2 focus:ring-indigo-500">

            <div class="grid grid-cols-2 gap-3">
                <button onclick="addEntry('expense')" class="bg-red-100 text-red-600 font-bold p-3 rouransition-colors">Потратил</button>
                <button onclick="addEntry('income')" class="bg-green-100 text-green-600 font-bold p-3 rounded-xl hover:bg-green-200 transition-colors">Отложил</button>
            </div>
        </div>
    </div>

    <!-- History Section -->
    <div class="flex justify-between items-center mb-4">
        <h2 class="text-lg font-semibold text-gray-700">История</h2>
    </div>

    <div id="historyList" class="flex flex-col gap-3">
        <!-- Entries will appear here -->
    </div>

    <script>
        const tg = window.Telegram.WebApp;
        tg.expand();

        // ТЕПЕРЬ ЗДЕСЬ ВАША РЕАЛЬНАЯ ССЫЛКА ОТ RENDER
        const API_URL = "https://my-money-bot-h4g2.onrender.com";
        const userId = tg.initDataUnsafe?.user?.id || "test_user";

        async function updateUI() {
            try {
                const balanceRes = await fetch(`${API_URL}/balance/${userId}`);
                const balanceData = await balanceRes.json();
                document.getElementById('totalBalance').innerText = `${balanceData.balance} ₽`;

                const historyRes = await fetch(`${API_URL}/history/${userId}`);
                const entries = await historyRes.json();

                const list = document.getElementById('historyList');
                list.innerHTML = '';

                entries.forEach(entry => {
                    const isIncome = entry.type === 'income';
                    const date = new Date(entry.timestamp).toLocaleDateString('ru-RU', {
                        day: 'numeric',
                        month: 'short'
                    });

                    const item = document.createElement('div');
                    item.className = `bg-white p-4 rounded-2xl shadow-sm flex justify-between items-center`;
                    item.innerHTML = `
                        <div class="flex flex-col">
                            <span class="text-xs text-gray-400">${date}</span>
                            <span class="text-sm text-gray-600">${entry.comment || 'Без комментария'}</span>
                        </div>
                        <div class="flex items-center gap-3">
                            <span class="font-bold ${isIncome ? 'text-green-500' : 'text-red-500'}">
                                ${isIncome ? '+' : '-'}${entry.amount} ₽
                            </span>
                            <button onclick="deleteEntry(${entry.id})" class="text-gray-300 hover:text-red-400 text-lg">&times;</button>
                        </div>
                    `;
                    list.appendChild(item);
                });
            } catch (e) {
                console.error("Ошибка обновления данных:", e);
            }
        }

        async function addEntry(type) {
            const amountInput = document.getElementById('amount');
            const commentInput = document.getElementById('comment');
            const amount = parseFloat(amountInput.value);
            const comment = commentInput.value.trim();

            if (isNaN(amount) || amount <= 0) {
                alert('Введите корректную сумму');
                return;
            }

            await fetch(`${API_URL}/add`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    user_id: userId,
                    amount: amount,
                    comment: comment,
                    type: type
                })
            });

            amountInput.value = '';
            commentInput.value = '';
            updateUI();
        }

        async function deleteEntry(id) {
            await fetch(`${API_URL}/delete/${id}`, { method: 'DELETE' });
            updateUI();
        }

        updateUI();
    </script>
</body>
</html>

Что делать дальше:
1. Сохраните этот код в money_webapp.html на GitHub.
2. Подождите 2 минуты, пока Render обновит сайт.
3. Открывайте своего бота в Telegram $\rightarrow$ Кнопка Меню $\rightarrow$ Готово!

Напишите, как только всё заработает! 😊

✻ Worked for 6s · done 8:39 · 1 shell still running

※ recap: We are building a Telegram Mini App for tracking daily expenses. The backend is deployed on Render, and the final step is for you to update the HTML file on GitHub to link them.

❯ я кнопку меню переименовал на Кошелёк

Это отличное решение! Название «Кошелёк» звучит гораздо приятнее и профессиональнее, чем просто «Меню». Теперь ваше приложение выглядит как настоящий финансовый продукт.

Теперь всё готово к запуску!

Если вы уже обновили код в money_webapp.html на GitHub и настроили кнопку в BotFather, то ваш «Кошелёк» должен работать.

Последний чек-лист для проверки:
1. В GitHub файл money_webapp.html сохранен с ссылкой https://my-money-bot-h4g2.onrender.com.
2. В BotFather ссылка на кнопку — https://my-money-bot-h4g2.onrender.com/.
3. Вы нажали кнопку «Кошелёк» в своем боте.

Попробуйте прямо сейчас добавить первую сумму. Если баланс обновился и запись появилась в истории — значит, мы это сделали! 🚀

Напишите, всё ли работает!

✻ Worked for 2s · done 8:43 · 1 shell still running

❯ в приложении пишет {"error":"Frontend file not found on server"}

Это значит, что сервер запустился, но он не может найти файл с сайтом. В облаке Render пути работают немного иначе, чем на вашем компьютере.

Скорее всего, сервер ищет файл в одной папке, а GitHub положил его в другую. Давайте исправим это одним раз и навсегда.

Я перепишу main.py так, чтобы он был максимально «умным» и искал ваш файл везде, где только можно, пока не найдет.

Пожалуйста, замените весь код в main.py на GitHub на этот:

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

# УЛУЧШЕННЫЙ ПОИСК ФАЙЛА
@app.get("/")
async def read_index():
    # Проверяем несколько возможных путей, где Render может хранить файл
    possible_paths = [
        "money_webapp.html",
        "./money_webapp.html",
        "/app/money_webapp.html",
        "static/money_webapp.html"
    ]

    for path in possible_paths:
        if os.path.exists(path):
            return FileResponse(path)

    return {"error": f"Frontend file not found. Checked paths: {possible_paths}"}

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)
