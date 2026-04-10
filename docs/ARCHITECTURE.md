# Sancta Stack Architecture

## Service Design Principles

### 1. Stateless Where Possible
Services should use external volumes for data persistence, not local storage.

### 2. REST API
All services expose a simple REST API over HTTP.

### 3. Health Checks
Every service implements `/health` endpoint for Docker and monitor integration.

### 4. Embedded Data Priority
Services include necessary data in the container image where possible for offline use.

### 5. Vector Search
Services with searchable content (scripture, catechism) include semantic search via embeddings.

## API Conventions

### Response Format
```json
{
  "success": true,
  "data": { ... },
  "meta": {
    "query_time_ms": 23,
    "version": "1.0.0"
  }
}
```

### Error Format
```json
{
  "success": false,
  "error": {
    "code": "NOT_FOUND",
    "message": "Resource not found"
  }
}
```

### Standard Endpoints
- `GET /health` - Service health
- `GET /info` - Service metadata and version
- `GET /search?q=...` - Search (if applicable)

## Cross-Service Communication

Services communicate directly via HTTP:
- Service discovery: Static config (Docker Compose) or mDNS (.local)

## Data Flow Example: Scripture + Doctrine

1. User query: "What does the Church teach about the Trinity?"
2. `doctrina` service: Semantic search for Trinity catechism entries
3. `scriptura` service: Search for Trinity-related verses
4. Agent combines and synthesizes response

## Technology Choices

| Service | Language | Data Store | Search |
|---------|----------|------------|--------|
| bede | Node.js | - (compute only) | - |
| scriptura | Python | SQLite | sqlite-vss or Chroma |
| doctrina | Python | JSON/SQLite | sqlite-vss |
| sancti | Python | SQLite | Standard SQL |
| oratio | Python | JSON | - |

## Docker Strategy

### Base Images
- Python: `python:3.12-slim`
- Node.js: `node:20-alpine`

### Multi-stage builds for smaller images
### Health checks in compose

## Security

- No external API keys required (public domain data)
- Local network only by default (.lan domains)
- Optional HTTPS via reverse proxy (nginx/traefik)
