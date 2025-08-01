from typing import Dict, Any
from fastapi import HTTPException, Depends
import httpx

from app.config import NYLAS_MESSAGES_ENDPOINT, logger
from app.auth.auth import get_access_token
from app.metrics.metrics import (
    track_request_success, 
    track_request_failure, 
    track_request_error, 
    get_request_latency_context,
    update_message_metrics
)


async def get_nylas_messages(token: str = Depends(get_access_token)) -> Dict[str, Any]:
    with get_request_latency_context('messages'):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    NYLAS_MESSAGES_ENDPOINT,
                    headers={"Authorization": f"Bearer {token}"}
                )
                
            if response.status_code == 200:
                track_request_success('messages')
                data = response.json()
                
                update_message_metrics(
                    data.get("totalMessages30d", 0),
                    data.get("unreadMessages", 0)
                )
                
                return data
            else:
                track_request_failure('messages')
                logger.error(f"Failed to get messages: {response.text}")
                raise HTTPException(status_code=response.status_code, detail="Failed to get messages")
        except Exception as e:
            track_request_error('messages')
            logger.error(f"Error getting messages: {e}")
            raise HTTPException(status_code=500, detail=f"Error getting messages: {str(e)}")