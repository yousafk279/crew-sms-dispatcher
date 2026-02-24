import os, sqlite3, asyncio, csv, io
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse, StreamingResponse
from twilio.rest import Client

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Portfolio Logic: Check if credentials exist
SID = os.getenv("TWILIO_ACCOUNT_SID")
TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
NUMBER = os.getenv("TWILIO_NUMBER")
PIN = os.getenv("ADMIN_PIN", "1234") 

def init_db():
    conn = sqlite3.connect('crew.db')
    conn.execute("CREATE TABLE IF NOT EXISTS alerts (message TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)")
    conn.commit()
    conn.close()

init_db()

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/send_sms")
async def send_sms(alert: str = Form(...), pin: str = Form(...)):
    if pin != PIN:
        return JSONResponse(content={"status": "Error", "message": "Invalid Admin PIN!"}, status_code=403)
    
    try:
        conn = sqlite3.connect('crew.db')
        conn.execute("INSERT INTO alerts (message) VALUES (?)", (alert,))
        conn.commit()
        conn.close()

        if SID and TOKEN and NUMBER:
            client = Client(SID, TOKEN)
            client.messages.create(body=alert, from_=NUMBER, to="+923000000000") 
            return JSONResponse(content={"status": "Success", "message": "Real SMS Sent!"})
        else:
            await asyncio.sleep(1.5) 
            return JSONResponse(content={"status": "Demo", "message": "Demo Mode: Alert saved to Database."})
            
    except Exception as e:
        return JSONResponse(content={"status": "Error", "message": f"System Error: {str(e)}"}, status_code=500)

@app.get("/history")
async def get_history():
    conn = sqlite3.connect('crew.db')
    rows = conn.execute("SELECT message, timestamp FROM alerts ORDER BY timestamp DESC LIMIT 10").fetchall()
    conn.close()
    return [{"message": r[0], "time": r[1]} for r in rows]

# NEW: CSV Export Logic
@app.get("/export")
async def export_csv():
    conn = sqlite3.connect('crew.db')
    cursor = conn.cursor()
    cursor.execute("SELECT message, timestamp FROM alerts ORDER BY timestamp DESC")
    rows = cursor.fetchall()
    conn.close()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Message", "Timestamp"]) 
    writer.writerows(rows)
    output.seek(0)

    return StreamingResponse(
        io.BytesIO(output.getvalue().encode()),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=dispatch_logs.csv"}
    )
