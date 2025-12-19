# Flask E-commerce Application - Docker Deployment Guide

This guide provides instructions for deploying the Flask e-commerce application (Lab 4 & 5) with SQLite database using Docker and Docker Compose.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Deployment](#deployment)
- [Database Persistence](#database-persistence)
- [Health Checks](#health-checks)
- [Application Features](#application-features)
- [Troubleshooting](#troubleshooting)

## Prerequisites

Before you begin, ensure you have the following installed:
- Docker (version 20.10 or later)
- Docker Compose (version 2.0 or later)

To verify your installation:
```bash
docker --version
docker compose --version
```

## Quick Start

1. Clone the repository:
```bash
git clone <repository-url>
cd Laboratorni
```

2. Build and start the application:
```bash
docker compose up -d
```

3. Verify the application is running:
```bash
docker compose ps
curl http://localhost:5000/
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

## Deployment

### Using Docker Compose (Recommended)

**Start the application:**
```bash
docker compose up -d
```

**View logs:**
```bash
docker compose logs -f flask-app
```

**Stop the application:**
```bash
docker compose down
```

**Rebuild after code changes:**
```bash
docker compose up -d --build
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

# Copy database from container
docker compose exec flask-app cat /app/data/app.db > backups/app.db.$(date +%Y%m%d_%H%M%S)
```

## Health Checks

The application includes built-in health checks that verify the application is responding.

### Check Health Status

**Via HTTP endpoint:**
```bash
curl http://localhost:5000/
```

**Via Docker:**
```bash
docker compose ps
```

Look for the "Status" column - healthy containers show `Up (healthy)`.

## Application Features

### Web Interface

- **Home Page** (`/`) - Featured products and store information
- **Product Catalog** (`/catalog`) - Browse all products by category
- **Shopping Cart** (`/cart`) - View and manage cart items
- **Reviews** (`/reviews`) - Customer reviews and feedback
- **Admin Panel** (`/admin`) - Manage products, orders, and clients
  - Default credentials: `admin` / `admin123`

### REST API Endpoints

**System:**
- `GET /api/health` - Health check
- `GET /api/docs` - Interactive Swagger documentation

**Products:**
- `GET /api/products` - List all products
- `POST /api/products` - Create product (admin)
- `PUT /api/products/<id>` - Update product (admin)
- `DELETE /api/products/<id>` - Delete product (admin)

**Orders & Feedback:**
- `GET /api/orders` - List all orders
- `GET /api/feedback` - List all feedback
- `POST /api/feedback` - Submit feedback

### API Documentation

Access the interactive Swagger/OpenAPI documentation at:
```
http://localhost:5000/api/docs
```

## Troubleshooting

### Container Won't Start

**Check logs:**
```bash
docker compose logs flask-app
```

**Common issues:**
- Port already in use: Change `HOST_PORT` in `.env`

### Database Errors

**Reset the database:**
```bash
docker compose down
docker volume rm laboratorni_sqlite-data
docker compose up -d
```

The application will automatically recreate the database with seed data.

## Production Deployment

For production environments, consider:

1. **Use a reverse proxy** (nginx) for SSL/TLS termination
2. **Set strong SECRET_KEY** in environment variables
3. **Regular backups** of the SQLite database
4. **Monitor health checks**
5. **Update admin credentials** from defaults
