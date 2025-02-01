from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
import time
import sqlite3
import logging

app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)


# Database connection
def get_db_connection():
    conn = sqlite3.connect('inventory.db')
    conn.row_factory = sqlite3.Row
    return conn


# Schemas
class TransformData(BaseModel):
    object: str
    transform: dict


class Item(BaseModel):
    name: str
    quantity: int


# Helper function for logging requests
def log_request(endpoint: str, data: dict):
    logging.info(f"Received request to {endpoint} with data: {data}")


# Routes
@app.post("/transform", status_code=200)
def transform(data: TransformData, background_tasks: BackgroundTasks):
    background_tasks.add_task(simulate_delay)
    log_request("/transform", data.model_dump())
    return {"status": "success", "data": data}


@app.post("/translation", status_code=200)
def translation(data: TransformData, background_tasks: BackgroundTasks):
    background_tasks.add_task(simulate_delay)
    log_request("/translation", data.model_dump())
    return {"status": "success", "position": data.transform['position']}


@app.post("/rotation", status_code=200)
def rotation(data: TransformData, background_tasks: BackgroundTasks):
    background_tasks.add_task(simulate_delay)
    log_request("/rotation", data.model_dump())
    return {"status": "success", "rotation": data.transform['rotation']}


@app.post("/scale", status_code=200)
def scale(data: TransformData, background_tasks: BackgroundTasks):
    background_tasks.add_task(simulate_delay)
    log_request("/scale", data.model_dump())
    return {"status": "success", "scale": data.transform['scale']}


@app.get("/file-path", status_code=200)
def file_path(background_tasks: BackgroundTasks, projectpath: bool = False):
    background_tasks.add_task(simulate_delay)
    log_request("/file-path", {"projectpath": projectpath})
    if projectpath:
        return {"path": "/path/to/project/folder"}
    return {"path": "/path/to/current/file"}


@app.post("/add-item", status_code=201)
def add_item(item: Item, background_tasks: BackgroundTasks):
    background_tasks.add_task(simulate_delay)
    log_request("/add-item", item.model_dump())
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO inventory (name, quantity) VALUES (?, ?)",
        (item.name, item.quantity)
    )
    conn.commit()
    conn.close()
    return {"status": "success", "item": item}


@app.post("/remove-item", status_code=200)
def remove_item(item: Item, background_tasks: BackgroundTasks):
    background_tasks.add_task(simulate_delay)
    log_request("/remove-item", item.model_dump())
    conn = get_db_connection()
    cursor = conn.execute(
        "DELETE FROM inventory WHERE name = ?",
        (item.name,)
    )
    conn.commit()
    conn.close()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"status": "success", "item": item.name}


@app.post("/update-quantity", status_code=200)
def update_quantity(item: Item, background_tasks: BackgroundTasks):
    background_tasks.add_task(simulate_delay)
    log_request("/update-quantity", item.model_dump())
    conn = get_db_connection()
    cursor = conn.execute(
        "UPDATE inventory SET quantity = ? WHERE name = ?",
        (item.quantity, item.name)
    )
    conn.commit()
    conn.close()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"status": "success", "item": item.name}


# Simulate delay function for background tasks
def simulate_delay():
    time.sleep(10)
