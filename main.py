@app.get("/history")
async def get_history():
    import sqlite3
    conn = sqlite3.connect('crew.db') # Connecting to your existing DB
    cursor = conn.cursor()
    # Assuming your table is named 'alerts' based on your previous logic
    cursor.execute("SELECT message, timestamp FROM alerts ORDER BY timestamp DESC LIMIT 10")
    rows = cursor.fetchall()
    conn.close()
    return [{"message": r[0], "time": r[1]} for r in rows]
