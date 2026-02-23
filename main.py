import os
import sqlite3
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from twilio.rest import Client

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Twilio Credentials from Secrets
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_NUMBER = os.getenv("TWILIO_NUMBER")

# Database setup
def init_db():
    conn = sqlite3.connect('crew.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/send_sms")
async def send_sms(alert: str = Form(...)):
    try:
        # 1. Save alert to the database
        conn = sqlite3.connect('crew.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO alerts (message) VALUES (?)", (alert,))
        conn.commit()
        conn.close()

        # 2. Trigger Twilio (Placeholder for your blast logic)
        # client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        # client.messages.create(body=alert, from_=TWILIO_NUMBER, to="+YOUR_NUMBER")

        return JSONResponse(content={"status": "Success", "message": "Alert sent to all crew members!"})
    except Exception as e:
        return JSONResponse(content={"status": "Error", "message": str(e)}, status_code=500)

@app.get("/history")
async def get_history():
    try:
        # 3. Fetch the last 10 alerts for the UI
        conn = sqlite3.connect('crew.db')
        cursor = conn.cursor()
        cursor.execute("SELECT message, timestamp FROM alerts ORDER BY timestamp DESC LIMIT 10")
        rows = cursor.fetchall()
        conn.close()
        return [{"message": r[0], "time": r[1]} for r in rows]
    except Exception as e:
        return JSONResponse(content={"status": "Error", "message": str(e)}, status_code=500)
