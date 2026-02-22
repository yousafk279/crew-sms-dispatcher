import os
import sqlite3
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from twilio.rest import Client
from dotenv import load_dotenv

# Load secrets from the hidden .env file
load_dotenv()

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Professional Secret Management
TWILIO_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_NUMBER = os.getenv('TWILIO_NUMBER')

def init_db():
    conn = sqlite3.connect('crew.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS crew (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            role TEXT NOT NULL,
            phone_number TEXT NOT NULL UNIQUE
        )
    ''')
    conn.commit()
    conn.close()

# Start database on launch
init_db()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/send-alert/")
async def send_alert(message: str = Form(...)):
    client = Client(TWILIO_SID, TWILIO_TOKEN)
    conn = sqlite3.connect('crew.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name, phone_number FROM crew')
    crew_list = cursor.fetchall()
    
    for name, phone in crew_list:
        try:
            client.messages.create(
                body=f"Hi {name}, {message}",
                from_=TWILIO_NUMBER,
                to=phone
            )
        except Exception as e:
            print(f"Failed for {name}: {e}")
            
    conn.close()
    return {"status": "Success", "message": "Alert sent to all crew members!"}