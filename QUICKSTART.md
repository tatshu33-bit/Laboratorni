# Quick Start Guide

Get the Flask SQLite application running in under 2 minutes!

## Prerequisites

- Docker 20.10+ 
- Docker Compose 2.0+

## Steps

### 1. Clone and Navigate
```bash
git clone <repository-url>
cd Laboratorni
```

### 2. Start the Application
```bash
docker compose up -d
```

### 3. Verify It's Running
```bash
# Check container status
docker compose ps

# Test health endpoint
curl http://localhost:5000/health
```

Expected output:
```json
{
  "status": "healthy",
  "database": "connected"
}
```

### 4. Try the API
```bash
# Create an item
curl -X POST http://localhost:5000/items \
  -H "Content-Type: application/json" \
  -d '{"name": "My First Item", "description": "Hello World!"}'

# List all items
curl http://localhost:5000/items
```

### 5. Run Tests (Optional)
```bash
./test_api.sh
```

## What's Next?

- **Full Documentation**: See [DEPLOYMENT.md](DEPLOYMENT.md) for complete deployment guide
- **Testing Guide**: See [TESTING.md](TESTING.md) for comprehensive testing instructions
- **Configuration**: Copy `.env.example` to `.env` to customize settings

## Common Commands

```bash
# View logs
docker compose logs -f flask-app

# Stop application
docker compose down

# Rebuild after changes
docker compose up -d --build

# Clean everything (including database)
docker compose down -v
```

## Troubleshooting

**Port already in use?**
```bash
# Change port in .env
echo "HOST_PORT=8080" > .env
docker compose up -d
```

**Container won't start?**
```bash
# Check logs
docker compose logs flask-app
```

**Need help?**
- Read [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions
- Read [TESTING.md](TESTING.md) for testing guidance

## Application Endpoints

- `GET /` - Application info
- `GET /health` - Health check
- `GET /items` - List all items
- `POST /items` - Create item
- `GET /items/<id>` - Get specific item
- `PUT /items/<id>` - Update item  
- `DELETE /items/<id>` - Delete item

---

**That's it!** Your Flask application with SQLite database is now running in a container with persistent storage. 🎉
