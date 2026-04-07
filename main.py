from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import sqlite3
from datetime import datetime

app = FastAPI(title="LogStreamer API")

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
@app.post("/logs")
def create_log(entry: LogEntry):
    print(f"GAVOME LOGĄ: {entry.source} | Lygis: {entry.level}")
    return {"status": "success", "data_received": entry}