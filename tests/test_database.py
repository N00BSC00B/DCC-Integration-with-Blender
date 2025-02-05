# filepath: /d:/Python/Blender Plugin/dcc-integration/tests/test_database.py
import pytest
from server.database import (
    add_item, remove_item, update_quantity, get_inventory,
    create_tables, Session
)


@pytest.fixture(scope="module", autouse=True)
def setup_database():
    create_tables()
    yield
    Session.remove()


def test_add_item():
    item = add_item("Test Item", 10)
    assert item.name == "Test Item"
    assert item.quantity == 10


def test_update_quantity():
    item = update_quantity("Test Item", 20)
    assert item.quantity == 20


def test_remove_item():
    item = remove_item("Test Item")
    assert item.name == "Test Item"


def test_get_inventory():
    inventory = get_inventory()
    assert len(inventory) == 0
