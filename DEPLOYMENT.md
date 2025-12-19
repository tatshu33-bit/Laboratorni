# Flask SQLite Application - Docker Deployment Guide

This guide provides instructions for deploying the Flask application with SQLite database using Docker and Docker Compose.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Deployment](#deployment)
- [Managing the Application](#managing-the-application)
- [Database Persistence](#database-persistence)
- [Health Checks](#health-checks)
- [API Endpoints](#api-endpoints)
- [Troubleshooting](#troubleshooting)

## Prerequisites

Before you begin, ensure you have the following installed:
- Docker (version 20.10 or later)
- Docker Compose (version 2.0 or later)

To verify your installation:
```bash
docker --version
docker-compose --version
```

## Quick Start

1. Clone the repository:
```bash
git clone <repository-url>
cd Laboratorni
```

2. Build and start the application:
```bash
docker-compose up -d
```

3. Verify the application is running:
```bash
docker-compose ps
curl http://localhost:5000/health
```

The application should be accessible at `http://localhost:5000`

## Configuration

### Environment Variables

The application can be configured using environment variables. Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit the `.env` file with your configuration:

| Variable | Description | Default |
|----------|-------------|---------|
| `HOST_PORT` | Port to expose on the host machine | `5000` |
| `SECRET_KEY` | Flask secret key for sessions | `change-this-secret-key-in-production` |
| `FLASK_ENV` | Flask environment (development/production) | `production` |
| `DATABASE_PATH` | SQLite database file path (inside container) | `/app/data/app.db` |

**⚠️ Security Note:** Always change the `SECRET_KEY` in production environments!

### Port Configuration

To change the port the application runs on:

1. Update `HOST_PORT` in your `.env` file:
```bash
HOST_PORT=8080
```

2. Restart the application:
```bash
docker-compose down
docker-compose up -d
```

## Deployment

### Option 1: Using Docker Compose (Recommended)

Docker Compose orchestrates the entire application stack.

**Start the application:**
```bash
docker-compose up -d
```

**View logs:**
```bash
docker-compose logs -f flask-app
```

**Stop the application:**
```bash
docker-compose down
```

**Rebuild after code changes:**
```bash
docker-compose up -d --build
```

### Option 2: Using Docker Directly

**Build the image:**
```bash
docker build -t flask-sqlite-app .
```

**Run the container:**
```bash
docker run -d \
  --name flask-app \
  -p 5000:5000 \
  -v sqlite-data:/app/data \
  -e SECRET_KEY=your-secret-key \
  flask-sqlite-app
```

## Managing the Application

### View Running Containers
```bash
docker-compose ps
```

### View Application Logs
```bash
# Follow logs in real-time
docker-compose logs -f flask-app

# View last 100 lines
docker-compose logs --tail=100 flask-app
```

### Restart the Application
```bash
docker-compose restart flask-app
```

### Stop and Remove Containers
```bash
# Stop containers
docker-compose stop

# Stop and remove containers
docker-compose down

# Stop and remove containers and volumes (⚠️ this deletes the database)
docker-compose down -v
```

### Execute Commands in the Container
```bash
# Open a shell in the running container
docker-compose exec flask-app sh

# Run a one-off command
docker-compose exec flask-app ls -la /app/data
```

## Database Persistence

### SQLite Volume

The SQLite database is stored in a Docker volume named `sqlite-data`. This ensures data persists even when containers are stopped or removed.

**Location inside container:** `/app/data/app.db`

### Backup the Database

**Create a backup:**
```bash
# Create backups directory
mkdir -p backups

# Copy database from container to host
docker-compose exec flask-app cat /app/data/app.db > backups/app.db.$(date +%Y%m%d_%H%M%S)
```

**Alternative method using docker cp:**
```bash
docker cp flask-sqlite-app:/app/data/app.db backups/app.db.backup
```

### Restore the Database

```bash
# Stop the application
docker-compose down

# Copy backup into volume
docker run --rm -v sqlite-data:/app/data -v $(pwd)/backups:/backup alpine \
  cp /backup/app.db.backup /app/data/app.db

# Start the application
docker-compose up -d
```

### Inspect Volume

```bash
# List volumes
docker volume ls

# Inspect the volume
docker volume inspect laboratorni_sqlite-data

# View volume contents
docker run --rm -v laboratorni_sqlite-data:/data alpine ls -la /data
```

## Health Checks

The application includes built-in health checks that verify:
- The Flask application is responding
- The SQLite database connection is working

### Check Health Status

**Via HTTP endpoint:**
```bash
curl http://localhost:5000/health
```

**Response (healthy):**
```json
{
  "status": "healthy",
  "database": "connected"
}
```

**Via Docker:**
```bash
docker-compose ps
```

Look for the "Status" column - healthy containers show `Up (healthy)`.

**View health check logs:**
```bash
docker inspect flask-sqlite-app | grep -A 10 Health
```

### Health Check Configuration

The health check runs every 30 seconds with the following parameters:
- **Interval:** 30 seconds
- **Timeout:** 3 seconds  
- **Start Period:** 5 seconds (grace period for startup)
- **Retries:** 3 attempts before marking unhealthy

## API Endpoints

### Root Endpoint
```bash
GET /
```
Returns application information and available endpoints.

**Example:**
```bash
curl http://localhost:5000/
```

### Health Check
```bash
GET /health
```
Returns application health status.

**Example:**
```bash
curl http://localhost:5000/health
```

### List Items
```bash
GET /items
```
Returns all items from the database.

**Example:**
```bash
curl http://localhost:5000/items
```

### Create Item
```bash
POST /items
Content-Type: application/json
```
Creates a new item.

**Example:**
```bash
curl -X POST http://localhost:5000/items \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Item", "description": "A test item"}'
```

### Get Item
```bash
GET /items/<id>
```
Returns a specific item.

**Example:**
```bash
curl http://localhost:5000/items/1
```

### Update Item
```bash
PUT /items/<id>
Content-Type: application/json
```
Updates an existing item.

**Example:**
```bash
curl -X PUT http://localhost:5000/items/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "Updated Item", "description": "Updated description"}'
```

### Delete Item
```bash
DELETE /items/<id>
```
Deletes an item.

**Example:**
```bash
curl -X DELETE http://localhost:5000/items/1
```

## Troubleshooting

### Container Won't Start

**Check logs:**
```bash
docker-compose logs flask-app
```

**Common issues:**
- Port already in use: Change `HOST_PORT` in `.env`
- Permission issues: Ensure Docker has proper permissions

### Database Errors

**Reset the database:**
```bash
docker-compose down
docker volume rm laboratorni_sqlite-data
docker-compose up -d
```

### Application Not Responding

**Check if container is running:**
```bash
docker-compose ps
```

**Check health status:**
```bash
curl http://localhost:5000/health
```

**Restart the application:**
```bash
docker-compose restart flask-app
```

### Can't Connect to Application

**Verify port mapping:**
```bash
docker-compose ps
```

**Check firewall:**
```bash
# Test from inside the container
docker-compose exec flask-app wget -O- http://localhost:5000/health
```

### Image Size Concerns

The Docker image is optimized using:
- Multi-stage builds (builder stage discarded)
- Alpine Linux base (minimal size)
- No-cache pip installations
- Minimal dependencies

**Check image size:**
```bash
docker images | grep flask-sqlite-app
```

### Performance Issues

**Monitor resource usage:**
```bash
docker stats flask-sqlite-app
```

**Increase resources if needed** (modify docker-compose.yml):
```yaml
services:
  flask-app:
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
```

## Production Deployment

For production environments, consider:

1. **Use a reverse proxy** (nginx, Traefik) for SSL/TLS termination
2. **Set strong SECRET_KEY** in environment variables
3. **Enable logging** to external systems
4. **Regular backups** of the SQLite database
5. **Monitor health checks** and set up alerts
6. **Use Docker secrets** for sensitive data
7. **Consider horizontal scaling** if needed (though SQLite has limitations)

### Example with nginx reverse proxy

```yaml
version: '3.8'

services:
  flask-app:
    # ... existing configuration ...
    expose:
      - "5000"
    # Remove ports section, let nginx handle external access

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./certs:/etc/nginx/certs:ro
    depends_on:
      - flask-app
```

## Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)

## Support

For issues and questions, please open an issue in the repository.
