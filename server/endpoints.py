from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import time
import sqlite3

app = FastAPI()

# Database connection
def get_db_connection():
    conn = sqlite3.connect('inventory.db')
    conn.row_factory = sqlite3.Row
    return conn

class TransformData(BaseModel):
    position: tuple
    rotation: tuple
    scale: tuple

@app.post("/transform")
async def transform(data: TransformData):
    time.sleep(10)  # Simulate delay
    print(f"Received transform data: {data}")
    return {"status": "success", "data": data}

@app.post("/translation")
async def translation(position: tuple):
    time.sleep(10)  # Simulate delay
    print(f"Received translation data: {position}")
    return {"status": "success", "position": position}

@app.post("/rotation")
async def rotation(rotation: tuple):
    time.sleep(10)  # Simulate delay
    print(f"Received rotation data: {rotation}")
    return {"status": "success", "rotation": rotation}

@app.post("/scale")
async def scale(scale: tuple):
    time.sleep(10)  # Simulate delay
    print(f"Received scale data: {scale}")
    return {"status": "success", "scale": scale}

@app.get("/file-path")
async def file_path(projectpath: bool = False):
    time.sleep(10)  # Simulate delay
    path = "/path/to/dcc/file" if not projectpath else "/path/to/project/folder"
    return {"file_path": path}

@app.post("/add-item")
async def add_item(name: str, quantity: int):
    time.sleep(10)  # Simulate delay
    conn = get_db_connection()
    conn.execute("INSERT INTO inventory (name, quantity) VALUES (?, ?)", (name, quantity))
    conn.commit()
    conn.close()
    print(f"Added item: {name}, quantity: {quantity}")
    return {"status": "success"}

@app.post("/remove-item")
async def remove_item(name: str):
    time.sleep(10)  # Simulate delay
    conn = get_db_connection()
    conn.execute("DELETE FROM inventory WHERE name = ?", (name,))
    conn.commit()
    conn.close()
    print(f"Removed item: {name}")
    return {"status": "success"}

@app.post("/update-quantity")
async def update_quantity(name: str, new_quantity: int):
    time.sleep(10)  # Simulate delay
    conn = get_db_connection()
    conn.execute("UPDATE inventory SET quantity = ? WHERE name = ?", (new_quantity, name))
    conn.commit()
    conn.close()
    print(f"Updated item: {name}, new quantity: {new_quantity}")
    return {"status": "success"}