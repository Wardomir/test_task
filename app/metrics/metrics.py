from fastapi import APIRouter
from fastapi.responses import JSONResponse
from prometheus_client import Counter, Histogram, Gauge, generate_latest
from prometheus_client.exposition import CONTENT_TYPE_LATEST


router = APIRouter()

REQUESTS_COUNTER = Counter('nylas_requests_total', 'Total number of requests', ['endpoint', 'status'])
AUTH_COUNTER = Counter('nylas_auth_total', 'Authentication attempts', ['status'])
REQUEST_LATENCY = Histogram('nylas_request_duration_seconds', 'Request latency in seconds', ['endpoint'])
DB_WRITES = Counter('nylas_db_writes_total', 'Number of successful DB writes')
MESSAGES_GAUGE = Gauge('nylas_total_messages', 'Total number of messages in last 30 days')
UNREAD_GAUGE = Gauge('nylas_unread_messages', 'Number of unread messages')


def track_auth_success():
    AUTH_COUNTER.labels('success').inc()


def track_auth_failure():
    AUTH_COUNTER.labels('failure').inc()


def track_auth_error():
    AUTH_COUNTER.labels('error').inc()


def track_request_success(endpoint: str):
    REQUESTS_COUNTER.labels(endpoint, 'success').inc()


def track_request_failure(endpoint: str):
    REQUESTS_COUNTER.labels(endpoint, 'failure').inc()


def track_request_error(endpoint: str):
    REQUESTS_COUNTER.labels(endpoint, 'error').inc()


def track_db_write():
    DB_WRITES.inc()


def update_message_metrics(total_messages: int, unread_messages: int):
    MESSAGES_GAUGE.set(total_messages)
    UNREAD_GAUGE.set(unread_messages)


def get_request_latency_context(endpoint: str):
    return REQUEST_LATENCY.labels(endpoint).time()


@router.get("/metrics")
async def metrics():
    return JSONResponse(
        content=generate_latest().decode("utf-8"),
        media_type=CONTENT_TYPE_LATEST
    )