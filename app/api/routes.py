from fastapi import APIRouter, BackgroundTasks, HTTPException
from fastapi.responses import RedirectResponse

from app.auth.auth import get_access_token
from app.auth.client import get_nylas_messages
from app.db.operations import store_messages_in_db
from app.config import logger


router = APIRouter()


@router.get("/")
async def root():
    return RedirectResponse(url="/docs")


@router.post("/fetch")
async def fetch_messages(background_tasks: BackgroundTasks, submitter: str = "system"):
    """This is an async approach to fetch messages as a task in the background."""
    try:
        background_tasks.add_task(fetch_and_store_messages, submitter)
        return {"status": "Processing", "message": "Fetching and storing messages in the background"}
    except Exception as e:
        logger.error(f"Error in fetch endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.get("/fetch-sync")
async def fetch_messages_sync(submitter: str = "system"):
    """This is a blocking sync approach to fetch messages where user must wait for the response."""
    try:
        token = await get_access_token()
        messages = await get_nylas_messages(token)
        row_id = await store_messages_in_db(messages, submitter)
        return {
            "status": "Success",
            "message": f"Messages fetched and stored with ID: {row_id}",
            "data": messages
        }
    except Exception as e:
        logger.error(f"Error in fetch-sync endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.get("/health")
async def health():
    return {"status": "healthy"}


async def fetch_and_store_messages(submitter: str = "system"):
    """An async task to fetch and store messages."""
    token = await get_access_token()
    messages = await get_nylas_messages(token)
    return await store_messages_in_db(messages, submitter)