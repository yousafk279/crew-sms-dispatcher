import os, sqlite3, asyncio
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from twilio.rest import Client

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Portfolio Logic: Check if credentials exist
SID = os.getenv("TWILIO_ACCOUNT_SID")
TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
NUMBER = os.getenv("TWILIO_NUMBER")
PIN = os.getenv("ADMIN_PIN", "1234") # Default PIN for portfolio visitors

def init_db():
    conn = sqlite3.connect('crew.db')
    conn.execute("CREATE TABLE IF NOT EXISTS alerts (message TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)")
    conn.commit()
    conn.close()

init_db()

@app.post("/send_sms")
async def send_sms(alert: str = Form(...), pin: str = Form(...)):
    # 1. Security Check
    if pin != PIN:
        return JSONResponse(content={"status": "Error", "message": "Invalid Admin PIN!"}, status_code=403)
    
    try:
        # 2. Database Logging (Always works)
        conn = sqlite3.connect('crew.db')
        conn.execute("INSERT INTO alerts (message) VALUES (?)", (alert,))
        conn.commit()
        conn.close()

        # 3. Smart API Logic
        if SID and TOKEN and NUMBER:
            # REAL MODE: If you ever add keys back, this runs automatically
            client = Client(SID, TOKEN)
            client.messages.create(body=alert, from_=NUMBER, to="+923000000000") # Replace with your verified number
            return JSONResponse(content={"status": "Success", "message": "Real SMS Sent via Twilio!"})
        else:
            # DEMO MODE: Perfect for Portfolios
            await asyncio.sleep(1.5) # Simulate network lag for realism
            return JSONResponse(content={
                "status": "Demo", 
                "message": "Demo Mode: Alert saved to Database. (Twilio credentials not configured by admin)."
            })
            
    except Exception as e:
        return JSONResponse(content={"status": "Error", "message": f"System Error: {str(e)}"}, status_code=500)

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/history")
async def get_history():
    conn = sqlite3.connect('crew.db')
    rows = conn.execute("SELECT message, timestamp FROM alerts ORDER BY timestamp DESC LIMIT 5").fetchall()
    conn.close()
    return [{"message": r[0], "time": r[1]} for r in rows]
