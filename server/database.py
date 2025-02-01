from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.exc import SQLAlchemyError
from contextlib import contextmanager

DATABASE_URL = "sqlite:///inventory.db"

# Initialize DB
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False
)
Base = declarative_base()

# Use scoped_session for thread-safe session management
Session = scoped_session(SessionLocal)


class Item(Base):
    """
    Represents an item in the database.
    Attributes:
        id (int): The unique id for the item. Auto-incremented primary key.
        name (str): The name of the item. Must be unique and cannot be null.
        quantity (int): The quantity of the item. Cannot be null.
    """
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    quantity = Column(Integer, nullable=False)


def create_tables():
    """
    Create database tables.
    This function initializes the database by creating all the tables defined
    in the metadata of the Base class. It uses the engine to connect to the
    database and execute the necessary SQL commands to create the tables.
    Returns:
        None
    """
    Base.metadata.create_all(engine)


@contextmanager
def get_database_session():
    """
    Provide a transactional scope around a series of operations.
    This function is a context manager that yields a SQLAlchemy session.
    It ensures that the session is committed if no exceptions occur,
    and rolled back if an SQLAlchemyError is raised. The session is
    always closed and expunged at the end of the transaction.
    Yields:
        Session: A SQLAlchemy session object.
    Raises:
        Exception: If a SQLAlchemyError occurs, an exception is raised
                   with the error message.
    """
    session = Session()
    try:
        yield session
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        raise Exception(f"Database error: {e}")
    finally:
        session.expunge_all()
        session.close()


def add_item(name: str, quantity: int):
    """
    Add a new item to the database.
    Args:
        name (str): The name of the item.
        quantity (int): The quantity of the item.
    Returns:
        Item: The newly added item with its latest state from the database.
    """
    with get_database_session() as session:
        new_item = Item(name=name, quantity=quantity)
        session.add(new_item)
        session.flush()
        session.refresh(new_item)
        return new_item


def remove_item(name: str):
    """
    Remove an item from the database by its name.
    Args:
        name (str): The name of the item to be removed.
    Returns:
        Item: The removed item if it was found and deleted.
    Raises:
        ValueError: If the item with the given name is not found.
    """
    with get_database_session() as session:
        item = session.query(Item).filter_by(name=name).first()
        if item:
            session.delete(item)
            return item
        raise ValueError("Item not found.")


def update_quantity(name: str, new_quantity: int):
    """
    Update the quantity of an item in the database.
    Args:
        name (str): The name of the item to update.
        new_quantity (int): The new quantity to set for the item.
    Returns:
        Item: The updated item with the new quantity.
    Raises:
        ValueError: If the item with the specified name is not found.
    """
    with get_database_session() as session:
        item = session.query(Item).filter_by(name=name).first()
        if item:
            item.quantity = new_quantity
            session.flush()  # Ensure changes are applied
            session.refresh(item)  # Refresh to get the latest state
            return item
        raise ValueError("Item not found.")


def get_inventory():
    """
    Retrieve all items from the inventory database.
    This function establishes a session with the database and queries all
    records from the Item table.
    Returns:
        list: A list of all items in the inventory.
    """
    with get_database_session() as session:
        return session.query(Item).all()
