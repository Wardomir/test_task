from datetime import datetime
from fastapi import HTTPException
import httpx

from app.config import (
    NYLAS_AUTH_ENDPOINT,
    NYLAS_CLIENT_ID,
    NYLAS_CLIENT_SECRET,
    logger
)
from app.metrics.metrics import track_auth_success, track_auth_failure, track_auth_error, get_request_latency_context


token_cache = {
    "access_token": None,
    "expires_at": None
}


async def get_access_token():
    if token_cache["access_token"] and token_cache["expires_at"] and token_cache["expires_at"] > datetime.now().timestamp():
        return token_cache["access_token"]
    
    with get_request_latency_context('auth'):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    NYLAS_AUTH_ENDPOINT,
                    json={
                        "client_id": NYLAS_CLIENT_ID,
                        "client_secret": NYLAS_CLIENT_SECRET
                    }
                )
                
            if response.status_code == 200:
                data = response.json()
                token_cache["access_token"] = data["access_token"]
                token_cache["expires_at"] = datetime.now().timestamp() + data["expires_in"]
                track_auth_success()
                return token_cache["access_token"]
            else:
                track_auth_failure()
                logger.error(f"Authentication failed: {response.text}")
                raise HTTPException(status_code=response.status_code, detail="Authentication failed")
        except Exception as e:
            track_auth_error()
            logger.error(f"Authentication error: {e}")
            raise HTTPException(status_code=500, detail=f"Authentication error: {str(e)}")