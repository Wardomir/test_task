# Nylas Integration Service

A FastAPI application that integrates with the Nylas API to fetch and store email messages. The service provides both synchronous and asynchronous endpoints for fetching messages, and includes Prometheus metrics for monitoring.

## Quick Start

To run the application, simply use Docker Compose:

```bash
docker compose up --build
```

This will:
1. Build the application container
2. Start a PostgreSQL database
3. Start the application on port 8000
4. Set up networking between the containers

Once running, you can access the API documentation at [http://localhost:8000/docs](http://localhost:8000/docs)

## API Endpoints

### Main Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Redirects to the API documentation |
| `/fetch` | POST | Asynchronously fetches messages from Nylas API and stores them in the database (non-blocking) |
| `/fetch-sync` | GET | Synchronously fetches messages from Nylas API and stores them in the database (blocking) |
| `/health` | GET | Health check endpoint |
| `/metrics` | GET | Prometheus metrics endpoint |

### Detailed API Description

#### `POST /fetch`

Asynchronously fetches messages from the Nylas API and stores them in the database. This endpoint returns immediately while processing continues in the background.

**Query Parameters:**
- `submitter` (optional): Identifier for who triggered the fetch (default: "system")

**Response:**
```json
{
  "status": "Processing",
  "message": "Fetching and storing messages in the background"
}
```

#### `GET /fetch-sync`

Synchronously fetches messages from the Nylas API and stores them in the database. This endpoint blocks until processing is complete.

**Query Parameters:**
- `submitter` (optional): Identifier for who triggered the fetch (default: "system")

**Response:**
```json
{
  "status": "Success",
  "message": "Messages fetched and stored with ID: {row_id}",
  "data": [
    {
      "id": "example-message-id",
      "subject": "Example Message",
      "sender": "sender@example.com",
      "received_at": "2025-08-01T12:00:00Z"
    }
  ]
}
```

#### `GET /health`

Health check endpoint to verify the service is running.

**Response:**
```json
{
  "status": "healthy"
}
```

#### `GET /metrics`

Returns Prometheus metrics for monitoring the application.

## Architecture

The application consists of:

- **FastAPI Application**: Handles HTTP requests and provides the API
- **PostgreSQL Database**: Stores fetched messages
- **Nylas Integration**: Connects to the Nylas API to fetch email messages
- **Prometheus Metrics**: Tracks application performance and usage

## Metrics

The application tracks the following metrics:

- Authentication attempts (success/failure/error)
- API requests by endpoint and status
- Request latency
- Database writes
- Total message count
- Unread message count

## Environment Variables

The application uses the following environment variables (set in docker-compose.yml):

- `DB_HOST`: PostgreSQL host
- `DB_PORT`: PostgreSQL port
- `DB_NAME`: PostgreSQL database name
- `DB_USER`: PostgreSQL username
- `DB_PASSWORD`: PostgreSQL password
- `NYLAS_BASE_URL`: URL for the Nylas API

## Development

To run the application in development mode:

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application: `python main.py`

For production use, the Docker Compose setup is recommended.