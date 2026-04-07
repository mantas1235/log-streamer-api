from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import sqlite3
from datetime import datetime
from fastapi import Security, HTTPException, status, Depends
from fastapi.security import APIKeyHeader
import os
from dotenv import load_dotenv

load_dotenv()





app = FastAPI(title="LogStreamer API")
API_key = os.getenv("SUPER_SECRET_KEY")
api_key_header = APIKeyHeader(name="X-API-Key")


def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key != API_key:
        raise HTTPException(
            status_code.HTTP_401_UNAUTHORIZED,
            detail = "Neteisingas API rkatas arba neturite teisių"
        )

    return api_key


def init_db():
    conn = sqlite3.connect("logs.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source TEXT,
    level TEXT,
    message TEXT,
    stack_trace TEXT,
    timestamp TEXT
    )
    """)

    conn.commit()
    conn.close()


init_db()

# Duomenų modelis
class LogEntry(BaseModel):
    source: str
    level: str
    message: str
    stack_trace: Optional[str] = None

# Mėlynas GET mygtukas
@app.get("/")
def read_root():
    return {"status": "online", "message": "LogStreamer API v1.0"}

# Žalias POST mygtukas
@app.post("/logs", dependencies=[Depends(verify_api_key)])
def create_log(entry: LogEntry):
    conn = sqlite3.connect("logs.db")
    cursor = conn.cursor()

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


    cursor.execute("""
    INSERT INTO logs (source,level,message,stack_trace,timestamp) VALUES (?,?,?,?,?)
    """, (entry.source, entry.level,entry.message, entry.stack_trace, timestamp))

    conn.commit()
    conn.close()

    return{"status": "Success", "message": "Log s4kmingai i6saugotas duomen7 baz4je"}

@app.get("/logs", dependencies=[Depends(verify_api_key)])
def get_logs(level: Optional[str]= None):
    conn = sqlite3.Connection("logs.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    if level:
        cursor.execute("SELECT * FROM logs WHERE level = ?", (level,))
    else:
        cursor.execute("SELECT * FROM logs")


    rows = cursor.fetchall()
    conn.close()


    logs_list = [dict(row) for row in rows]
    return {"status": "success", "total_logs": len(logs_list), "data": logs_list}