import pytest
from fastapi.testclient import TestClient
from server import endpoints
from fastapi import FastAPI

app = FastAPI()
app.include_router(endpoints.router)

client = TestClient(app)


@pytest.fixture
def test_client():
    return client


def test_add_item(test_client):
    response = test_client.post(
        "/add-item",
        json={"name": "Test Item", "quantity": 10}
    )
    assert response.status_code == 201
    assert response.json() == {
        "status": "success",
        "item": {"name": "Test Item", "quantity": 10}
    }


def test_update_quantity(test_client):
    response = test_client.post(
        "/update-quantity",
        json={"name": "Test Item", "new_quantity": 20}
    )
    assert response.status_code == 200
    assert response.json() == {
        "status": "success",
        "item": {"name": "Test Item", "quantity": 20}
    }


def test_remove_item(test_client):
    response = test_client.post(
        "/remove-item",
        json={"name": "Test Item"}
    )
    assert response.status_code == 200
    assert response.json() == {"status": "success", "item": "Test Item"}


def test_get_inventory(test_client):
    response = test_client.get("/get_inventory")
    assert response.status_code == 200
    assert "inventory" in response.json()
    assert response.json()["status"] == "success"


def test_transform(test_client):
    response = test_client.post(
        "/transform",
        json={"object": "cube", "transform": {"scale": 2}}
    )
    assert response.status_code == 200
    assert response.json() == {
        "status": "success",
        "data": {"object": "cube", "transform": {"scale": 2}}
    }


def test_translation(test_client):
    response = test_client.post(
        "/translation",
        json={"object": "cube", "transform": {"position": [1, 2, 3]}}
    )
    assert response.status_code == 200
    assert response.json() == {"status": "success", "position": [1, 2, 3]}


def test_rotation(test_client):
    response = test_client.post(
        "/rotation",
        json={"object": "cube", "transform": {"rotation": [90, 0, 0]}}
    )
    assert response.status_code == 200
    assert response.json() == {"status": "success", "rotation": [90, 0, 0]}


def test_scale(test_client):
    response = test_client.post(
        "/scale",
        json={"object": "cube", "transform": {"scale": 2}}
    )
    assert response.status_code == 200
    assert response.json() == {"status": "success", "scale": 2}


def test_file_path(test_client):
    response = test_client.get("/file-path")
    assert response.status_code == 200
    assert response.json() == {"path": "/path/to/current/file"}

    response = test_client.get("/file-path?projectpath=true")
    assert response.status_code == 200
    assert response.json() == {"path": "/path/to/project/folder"}
