import uvicorn
from fastapi import FastAPI
from .endpoints import router
from .database import create_tables

# Initialize FastAPI app
app = FastAPI()

# Create tables on startup
create_tables()

# Include all routes from endpoints.py
app.include_router(router)

# Run FastAPI with Uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
