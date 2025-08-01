from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.api.routes import router as api_router
from app.metrics.metrics import router as metrics_router
from app.db.operations import create_db_and_tables
from app.config import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize services before application starts
    logger.info("Starting up Nylas Integration Service")
    create_db_and_tables()
    
    yield
    
    # Shutdown: Clean up resources when application is shutting down
    logger.info("Shutting down Nylas Integration Service")


app = FastAPI(title="Nylas Integration Service", lifespan=lifespan)


app.include_router(api_router)
app.include_router(metrics_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
