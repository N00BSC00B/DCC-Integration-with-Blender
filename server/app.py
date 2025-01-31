from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import time
import logging
from .database import Database

app = FastAPI()

# Middleware to allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the database
database = Database()

@app.post("/transform")
async def transform(data: dict):
    time.sleep(10)  # Simulate delay
    logging.info(f"Received transform data: {data}")
    # Process transform data
    return {"status": "success"}

@app.post("/translation")
async def translation(data: dict):
    time.sleep(10)  # Simulate delay
    logging.info(f"Received translation data: {data}")
    return {"status": "success"}

@app.post("/rotation")
async def rotation(data: dict):
    time.sleep(10)  # Simulate delay
    logging.info(f"Received rotation data: {data}")
    return {"status": "success"}

@app.post("/scale")
async def scale(data: dict):
    time.sleep(10)  # Simulate delay
    logging.info(f"Received scale data: {data}")
    return {"status": "success"}

@app.get("/file-path")
async def file_path(projectpath: bool = False):
    time.sleep(10)  # Simulate delay
    logging.info("Requested file path")
    if projectpath:
        return {"path": "project_folder_path"}
    return {"path": "current_file_path"}

@app.post("/add-item")
async def add_item(item: dict):
    time.sleep(10)  # Simulate delay
    logging.info(f"Adding item: {item}")
    # Add item to database
    return {"status": "item added"}

@app.post("/remove-item")
async def remove_item(item_name: str):
    time.sleep(10)  # Simulate delay
    logging.info(f"Removing item: {item_name}")
    # Remove item from database
    return {"status": "item removed"}

@app.post("/update-quantity")
async def update_quantity(item: dict):
    time.sleep(10)  # Simulate delay
    logging.info(f"Updating quantity for item: {item}")
    # Update item quantity in database
    return {"status": "quantity updated"}