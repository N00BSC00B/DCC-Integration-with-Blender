import logging
import asyncio
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from .database import add_item, remove_item, update_quantity, get_inventory

# Initialize Router
router = APIRouter()

# Configure logging
logging.basicConfig(level=logging.INFO)


def log_request(endpoint: str, data: dict):
    """
    Logs an incoming request to a specified endpoint with the provided data.
    Args:
        endpoint (str): The endpoint that received the request.
        data (dict): The data associated with the request.
    Returns:
        None
    """
    logging.info(f"Received request to {endpoint} with data: {data}")


# Request Models
class TransformData(BaseModel):
    object: str
    transform: dict


class AddItem(BaseModel):
    name: str
    quantity: int


class RemoveItem(BaseModel):
    name: str


class UpdateItem(BaseModel):
    name: str
    new_quantity: int


# Transformation Endpoints
@router.post("/transform", status_code=200)
async def transform(data: TransformData):
    """
    Asynchronously transforms the given data.
    Args:
        data (TransformData): The data to be transformed.
    Returns:
        dict: A dictionary containing the status of the transformation and the
        transformed data.
    """
    await asyncio.sleep(10)
    log_request("/transform", data.model_dump())
    return {"status": "success", "data": data}


@router.post("/translation", status_code=200)
async def translation(data: TransformData):
    """
    Handle the translation request.
    Args:
        data (TransformData): The transformation data containing the
        position information.
    Returns:
        dict: A dictionary containing the status of the request and the
        position data.
    """
    await asyncio.sleep(10)
    log_request("/translation", data.model_dump())
    return {"status": "success", "position": data.transform.get('position')}


@router.post("/rotation", status_code=200)
async def rotation(data: TransformData):
    """
    Handle the rotation endpoint.
    Args:
        data (TransformData): The transformation data containing the
        transformation information.
    Returns:
        dict: A dictionary containing the status of the request and the
        rotation data.
    """
    await asyncio.sleep(10)
    log_request("/rotation", data.model_dump())
    return {"status": "success", "rotation": data.transform.get('rotation')}


@router.post("/scale", status_code=200)
async def scale(data: TransformData):
    """
    Asynchronously scales a given transform data.
    Args:
        data (TransformData): The transformation data containing the
        scale information.
    Returns:
        dict: A dictionary containing the status of the request and the
        scale value.
    """
    await asyncio.sleep(10)
    log_request("/scale", data.model_dump())
    return {"status": "success", "scale": data.transform.get('scale')}


# File Path Endpoint
@router.get("/file-path", status_code=200)
async def file_path(projectpath: bool = False):
    """
    Asynchronously retrieves the file path based on the provided parameter.
    Args:
        projectpath (bool): If True, returns the path to the project folder.
                            If False, returns the path to the current file.
                            Defaults to False.
    Returns:
        dict: A dictionary containing the key 'path' with the corresponding
        file path as its value.
    """
    await asyncio.sleep(10)
    log_request("/file-path", {"projectpath": projectpath})
    if projectpath:
        return {"path": "/path/to/project/folder"}
    return {"path": "/path/to/current/file"}


# Inventory Endpoints
@router.post("/add-item", status_code=201)
async def add_inventory_item(item: AddItem):
    """
    Asynchronously adds an inventory item.
    If successful, it returns the added item's details.
    If an error occurs, it raises an HTTPException.
    Args:
        item (Item): The item to be added to the inventory.
    Returns:
        dict: A dictionary containing the status and the added item's details.
    Raises:
        HTTPException: If there is an error adding the item to the inventory.
    """
    await asyncio.sleep(10)
    log_request("/add-item", item.model_dump())
    try:
        added_item = add_item(item.name, item.quantity)
        return {
            "status": "success",
            "item": {
                "name": added_item.name,
                "quantity": added_item.quantity
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/remove-item", status_code=200)
async def remove_inventory_item(item: RemoveItem):
    """
    Asynchronously removes an inventory item.
    If successful, it returns the removed item's details.
    If an error occurs, it raises an HTTPException.
    Args:
        item (Item): The inventory item to be removed.
    Returns:
        dict: A dictionary containing the status of the operation and the name
              of the removed item if successful.
    Raises:
        HTTPException: If the item is not found (404) or if any other error
                       occurs (400).
    """
    await asyncio.sleep(10)
    log_request("/remove-item", item.model_dump())
    try:
        removed_item = remove_item(item.name)
        return {"status": "success", "item": removed_item.name}
    except ValueError:
        raise HTTPException(status_code=404, detail="Item not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/update-quantity", status_code=200)
async def update_inventory_quantity(item: UpdateItem):
    """
    Asynchronously updates the quantity of an inventory item.
    If successful, it returns the updated item's details.
    If an error occurs, it raises an HTTPException.
    Args:
        item (Item): The item object containing the name and quantity to be
        updated.
    Returns:
        dict: A dictionary containing the status of the update and the updated
        item details.
    Raises:
        HTTPException: If the item is not found (status code 404)
        or if any other error occurs (status code 400).
    """
    await asyncio.sleep(10)
    log_request("/update-quantity", item.model_dump())
    try:
        updated_item = update_quantity(item.name, item.new_quantity)
        return {
            "status": "success",
            "item": {
                "name": updated_item.name,
                "quantity": updated_item.quantity
            }
        }
    except ValueError:
        raise HTTPException(status_code=404, detail="Item not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/get_inventory", status_code=200)
async def get_inventory_items():
    """
    Asynchronously retrieves inventory items.
    Returns:
        dict: A dictionary containing the status of the request and a list
              of inventory items, where each item is represented as a
              dictionary with 'name' and 'quantity' keys.
    """
    log_request("/inventory", {})
    items = get_inventory()
    return {
        "status": "success",
        "inventory": [
            {"name": i.name, "quantity": i.quantity} for i in items
        ]
    }
