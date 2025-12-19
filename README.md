# Laboratorni

A containerized Flask web application with SQLite database, designed for easy deployment using Docker and Docker Compose.

## Features

- **Flask REST API** with CRUD operations
- **SQLite Database** with persistent storage
- **Docker Containerization** with optimized image size
- **Health Checks** for monitoring application status
- **Environment Variables** for flexible configuration
- **Docker Compose** orchestration

## Quick Start

```bash
# Build and start the application
docker-compose up -d

# Check the application status
curl http://localhost:5000/health

# View logs
docker-compose logs -f flask-app
```

The application will be available at `http://localhost:5000`

## Documentation

For complete deployment instructions, configuration options, and troubleshooting, see [DEPLOYMENT.md](DEPLOYMENT.md)

## API Endpoints

- `GET /` - Application information
- `GET /health` - Health check endpoint
- `GET /items` - List all items
- `POST /items` - Create a new item
- `GET /items/<id>` - Get a specific item
- `PUT /items/<id>` - Update an item
- `DELETE /items/<id>` - Delete an item

## Project Structure

```
.
├── app.py                 # Flask application
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker image definition
├── docker-compose.yml    # Docker Compose configuration
├── .dockerignore         # Files to exclude from Docker build
├── .env.example          # Example environment variables
├── DEPLOYMENT.md         # Complete deployment documentation
└── README.md            # This file
```

## Requirements

- Docker 20.10+
- Docker Compose 2.0+

## License

See repository license file.