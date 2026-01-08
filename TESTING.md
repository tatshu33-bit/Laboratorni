# Testing Guide

This document describes how to test the containerized Flask SQLite application.

## Prerequisites

- Docker and Docker Compose installed
- curl (for API testing)
- bash (for running test scripts)

## Quick Test

The simplest way to test the application:

```bash
# Start the application
docker compose up -d

# Wait for the application to be ready (check health status)
docker compose ps

# Run the automated test suite
./test_api.sh

# Stop the application
docker compose down
```

## Automated Testing

The repository includes an automated test script `test_api.sh` that validates all API endpoints.

### Running the Test Suite

```bash
# Make sure the application is running
docker compose up -d

# Wait a few seconds for startup
sleep 5

# Run tests
./test_api.sh
```

### Test Coverage

The test suite verifies:
- ✓ Root endpoint returns application info
- ✓ Health check endpoint returns healthy status
- ✓ List items endpoint (empty state)
- ✓ Create items via POST
- ✓ List items (with data)
- ✓ Get specific item by ID
- ✓ Update item via PUT
- ✓ Delete item
- ✓ Error handling (404 for missing items)
- ✓ Validation (400 for invalid requests)

## Manual Testing

### Test Health Check

```bash
curl http://localhost:5000/health
```

Expected response:
```json
{
  "status": "healthy",
  "database": "connected"
}
```

### Test Root Endpoint

```bash
curl http://localhost:5000/
```

Expected response:
```json
{
  "message": "Flask SQLite Application",
  "status": "running",
  "endpoints": {
    "/": "This page",
    "/health": "Health check endpoint",
    "/items": "GET: List all items, POST: Create item",
    "/items/<id>": "GET: Get item, PUT: Update item, DELETE: Delete item"
  }
}
```

### Test CRUD Operations

#### Create an Item
```bash
curl -X POST http://localhost:5000/items \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Item", "description": "A test item"}'
```

Expected response (HTTP 201):
```json
{
  "id": 1,
  "name": "Test Item",
  "description": "A test item"
}
```

#### List All Items
```bash
curl http://localhost:5000/items
```

Expected response (HTTP 200):
```json
{
  "items": [
    {
      "id": 1,
      "name": "Test Item",
      "description": "A test item",
      "created_at": "2025-12-19 12:00:00"
    }
  ]
}
```

#### Get a Specific Item
```bash
curl http://localhost:5000/items/1
```

Expected response (HTTP 200):
```json
{
  "id": 1,
  "name": "Test Item",
  "description": "A test item",
  "created_at": "2025-12-19 12:00:00"
}
```

#### Update an Item
```bash
curl -X PUT http://localhost:5000/items/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "Updated Item", "description": "Updated description"}'
```

Expected response (HTTP 200):
```json
{
  "id": 1,
  "message": "Item updated"
}
```

#### Delete an Item
```bash
curl -X DELETE http://localhost:5000/items/1
```

Expected response (HTTP 200):
```json
{
  "message": "Item deleted"
}
```

## Testing Database Persistence

To verify that data persists across container restarts:

```bash
# Start the application
docker compose up -d

# Create an item
curl -X POST http://localhost:5000/items \
  -H "Content-Type: application/json" \
  -d '{"name": "Persistent Item", "description": "This should survive restart"}'

# Stop the application
docker compose down

# Start again
docker compose up -d

# Verify the item still exists
curl http://localhost:5000/items
```

The item should still be present in the response.

## Testing Docker Health Checks

Docker Compose includes health checks that monitor the application status.

### Check Health Status
```bash
# View container status including health
docker compose ps

# Inspect health check details
docker inspect flask-sqlite-app | grep -A 10 Health

# View health check logs
docker inspect flask-sqlite-app --format='{{json .State.Health}}' | python3 -m json.tool
```

A healthy container will show:
```
NAME               STATUS           PORTS
flask-sqlite-app   Up (healthy)     0.0.0.0:5000->5000/tcp
```

### Force Health Check
```bash
# Manually trigger health check
docker exec flask-sqlite-app python -c "import urllib.request; print(urllib.request.urlopen('http://localhost:5000/health').read().decode())"
```

## Load Testing

For basic load testing, you can use `ab` (Apache Bench) or similar tools:

```bash
# Install Apache Bench (if not installed)
sudo apt-get install apache2-utils  # Ubuntu/Debian
# or
brew install httpd  # macOS

# Run 1000 requests with 10 concurrent connections
ab -n 1000 -c 10 http://localhost:5000/

# Test the health endpoint
ab -n 1000 -c 10 http://localhost:5000/health
```

## Testing in Different Environments

### Development Environment
```bash
# Use docker-compose with default settings
docker compose up
```

### Production-like Environment
```bash
# Create a .env file with production settings
cat > .env << EOF
HOST_PORT=80
SECRET_KEY=$(openssl rand -hex 32)
FLASK_ENV=production
EOF

# Start with production configuration
docker compose up -d
```

## Troubleshooting Tests

### Test Failures

If tests fail, check:

1. **Application not ready**: Wait longer before running tests
   ```bash
   sleep 10
   ./test_api.sh
   ```

2. **Port already in use**: Another service is using port 5000
   ```bash
   # Change port in .env
   echo "HOST_PORT=8080" >> .env
   docker compose up -d
   # Update test URLs to use port 8080
   ```

3. **Container not healthy**: Check logs
   ```bash
   docker compose logs flask-app
   ```

### Viewing Application Logs During Tests

```bash
# Follow logs in real-time
docker compose logs -f flask-app

# In another terminal, run tests
./test_api.sh
```

## Continuous Integration

For CI/CD pipelines, use:

```bash
#!/bin/bash
set -e

# Build and start
docker compose up -d --build

# Wait for health check
timeout 60 bash -c 'until docker compose ps | grep healthy; do sleep 2; done'

# Run tests
./test_api.sh

# Cleanup
docker compose down -v
```

## Performance Benchmarks

Expected performance on modern hardware:
- Health check response: < 10ms
- Simple GET requests: < 50ms
- POST/PUT/DELETE operations: < 100ms
- Concurrent requests (10 connections): > 100 requests/second

## Database Testing

### Inspect Database
```bash
# Access the database directly
docker compose exec flask-app sh

# Inside container, use sqlite3
cd /app/data
sqlite3 app.db

# Run SQL queries
sqlite> .tables
sqlite> SELECT * FROM items;
sqlite> .exit
```

### Test Volume Persistence
```bash
# Check volume exists
docker volume ls | grep laboratorni

# Inspect volume
docker volume inspect laboratorni_sqlite-data

# View volume contents
docker run --rm -v laboratorni_sqlite-data:/data alpine ls -lh /data
```

## Security Testing

### Test for SQL Injection
```bash
# Try SQL injection in item name
curl -X POST http://localhost:5000/items \
  -H "Content-Type: application/json" \
  -d '{"name": "Test'\'' OR 1=1--", "description": "SQL injection test"}'

# The application should handle this safely
```

### Test for XSS
```bash
# Try XSS in item description
curl -X POST http://localhost:5000/items \
  -H "Content-Type: application/json" \
  -d '{"name": "XSS Test", "description": "<script>alert(\"XSS\")</script>"}'

# Data should be stored as-is (API doesn't render HTML)
```

## Cleanup After Testing

```bash
# Stop and remove containers
docker compose down

# Remove volumes (deletes database)
docker compose down -v

# Remove images
docker rmi laboratorni-flask-app

# Remove test data directory
rm -rf data/
```

## Test Results Verification

All tests should pass with the following summary:
```
===================================
Test Results
===================================
Passed: 12
All tests passed!
```

If any tests fail, review the error messages and check:
- Container logs: `docker compose logs flask-app`
- Health status: `docker compose ps`
- Network connectivity: `curl -v http://localhost:5000/health`
