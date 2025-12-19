# Laboratorni REST API

A comprehensive REST API for managing laboratory items, built with Flask and documented using Swagger/OpenAPI.

## Features

- **6+ RESTful Endpoints** for complete CRUD operations
- **JSON Data Exchange** format
- **Comprehensive Error Handling** (400, 404, 500)
- **Interactive API Documentation** using Flasgger/Swagger
- **Postman Collection** for easy testing
- **Health Check Endpoint** for monitoring

## API Endpoints

### System Endpoints
- `GET /` - Welcome message and API info
- `GET /api/health` - Health check endpoint
- `GET /api/docs` - Interactive Swagger documentation

### Item Management Endpoints
- `GET /api/items` - Get all items (supports category filtering)
- `GET /api/items/<id>` - Get specific item by ID
- `POST /api/items` - Create a new item
- `PUT /api/items/<id>` - Update an existing item
- `DELETE /api/items/<id>` - Delete an item

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Laboratorni
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the API

Start the Flask development server:
```bash
python app.py
```

The API will be available at: `http://localhost:5000`

**Security Note:** By default, the API runs in debug mode for development. To run in production mode, set the environment variable:
```bash
export FLASK_DEBUG=False
python app.py
```

For production deployments, use a production WSGI server like Gunicorn or uWSGI instead of the Flask development server.

## API Documentation

Once the server is running, access the interactive Swagger documentation at:
```
http://localhost:5000/api/docs
```

The Swagger UI provides:
- Complete endpoint descriptions
- Request/response schemas
- Interactive testing interface
- Example requests and responses

## Testing with Postman

### Import Collection

1. Open Postman
2. Click "Import" button
3. Select the `Laboratorni_API_Collection.postman_collection.json` file
4. The collection will be imported with all test scenarios

### Test Scenarios Included

The Postman collection includes:

**System Tests:**
- Root endpoint verification
- Health check validation

**CRUD Operations Tests:**
- Retrieve all items
- Filter items by category
- Get specific item by ID
- Create new item with validation
- Update existing item (partial updates supported)
- Delete item

**Error Handling Tests:**
- 404 Not Found (non-existent items)
- 400 Bad Request (missing required fields)

### Running Tests

1. Ensure the API is running (`python app.py`)
2. In Postman, select the "Laboratorni REST API" collection
3. Click "Run" to execute all tests
4. Review results in the Collection Runner

## API Usage Examples

### Get All Items
```bash
curl -X GET http://localhost:5000/api/items
```

Response:
```json
{
  "count": 3,
  "items": [
    {
      "id": 1,
      "name": "Microscope",
      "category": "Equipment",
      "quantity": 5,
      "created_at": "2025-01-01T10:00:00"
    }
  ]
}
```

### Create New Item
```bash
curl -X POST http://localhost:5000/api/items \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Petri Dish",
    "category": "Glassware",
    "quantity": 50
  }'
```

Response:
```json
{
  "message": "Item created successfully",
  "item": {
    "id": 4,
    "name": "Petri Dish",
    "category": "Glassware",
    "quantity": 50,
    "created_at": "2025-12-19T14:58:00"
  }
}
```

### Update Item
```bash
curl -X PUT http://localhost:5000/api/items/1 \
  -H "Content-Type: application/json" \
  -d '{
    "quantity": 8
  }'
```

### Delete Item
```bash
curl -X DELETE http://localhost:5000/api/items/3
```

## Error Responses

The API returns consistent error responses:

```json
{
  "error": "Not Found",
  "message": "Item with ID 999 not found",
  "status": 404
}
```

Common status codes:
- `200` - Success
- `201` - Created
- `400` - Bad Request
- `404` - Not Found
- `500` - Internal Server Error

## Project Structure

```
Laboratorni/
├── app.py                                          # Main Flask application
├── requirements.txt                                 # Python dependencies
├── Laboratorni_API_Collection.postman_collection.json  # Postman tests
└── README.md                                        # This file
```

## Technology Stack

- **Flask 3.0.0** - Web framework
- **Flasgger 0.9.7.1** - Swagger/OpenAPI documentation
- **Python 3.8+** - Programming language

## Development Notes

- The API currently uses in-memory storage (data resets on restart)
- For production use, integrate a database (SQLite, PostgreSQL, etc.)
- Debug mode is enabled by default (disable for production)

## License

This project is part of laboratory coursework.