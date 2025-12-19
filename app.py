"""
Main Flask application for Laboratorni REST API
Implements a basic REST API with 6+ endpoints for item management
"""
from flask import Flask, jsonify, request
from flasgger import Swagger, swag_from
from datetime import datetime

app = Flask(__name__)

# Configure Swagger/OpenAPI documentation
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/api/docs"
}

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Laboratorni REST API",
        "description": "A comprehensive REST API for managing laboratory items",
        "version": "1.0.0",
        "contact": {
            "name": "API Support",
            "email": "support@laboratorni.com"
        }
    },
    "basePath": "/",
    "schemes": ["http", "https"],
}

swagger = Swagger(app, config=swagger_config, template=swagger_template)

# In-memory data store (simulating a database)
items = [
    {"id": 1, "name": "Microscope", "category": "Equipment", "quantity": 5, "created_at": "2025-01-01T10:00:00"},
    {"id": 2, "name": "Test Tubes", "category": "Glassware", "quantity": 100, "created_at": "2025-01-01T10:00:00"},
    {"id": 3, "name": "Bunsen Burner", "category": "Equipment", "quantity": 10, "created_at": "2025-01-01T10:00:00"},
]
next_id = 4


# Error handlers
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        "error": "Not Found",
        "message": "The requested resource was not found",
        "status": 404
    }), 404


@app.errorhandler(400)
def bad_request(error):
    """Handle 400 errors"""
    return jsonify({
        "error": "Bad Request",
        "message": str(error),
        "status": 400
    }), 400


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        "error": "Internal Server Error",
        "message": "An unexpected error occurred",
        "status": 500
    }), 500


# API Endpoints
@app.route('/')
def index():
    """
    Root endpoint
    ---
    responses:
      200:
        description: Welcome message
        schema:
          type: object
          properties:
            message:
              type: string
            documentation:
              type: string
    """
    return jsonify({
        "message": "Welcome to Laboratorni REST API",
        "documentation": "/api/docs"
    })


@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    ---
    tags:
      - System
    responses:
      200:
        description: API health status
        schema:
          type: object
          properties:
            status:
              type: string
              example: healthy
            timestamp:
              type: string
              example: 2025-12-19T14:58:00
            version:
              type: string
              example: 1.0.0
    """
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }), 200


@app.route('/api/items', methods=['GET'])
def get_items():
    """
    Get all items
    ---
    tags:
      - Items
    parameters:
      - name: category
        in: query
        type: string
        required: false
        description: Filter items by category
    responses:
      200:
        description: List of all items
        schema:
          type: object
          properties:
            count:
              type: integer
              example: 3
            items:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                  name:
                    type: string
                  category:
                    type: string
                  quantity:
                    type: integer
                  created_at:
                    type: string
    """
    category = request.args.get('category')
    
    if category:
        filtered_items = [item for item in items if item['category'].lower() == category.lower()]
        return jsonify({"count": len(filtered_items), "items": filtered_items}), 200
    
    return jsonify({"count": len(items), "items": items}), 200


@app.route('/api/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    """
    Get a specific item by ID
    ---
    tags:
      - Items
    parameters:
      - name: item_id
        in: path
        type: integer
        required: true
        description: ID of the item to retrieve
    responses:
      200:
        description: Item details
        schema:
          type: object
          properties:
            id:
              type: integer
            name:
              type: string
            category:
              type: string
            quantity:
              type: integer
            created_at:
              type: string
      404:
        description: Item not found
        schema:
          type: object
          properties:
            error:
              type: string
            message:
              type: string
            status:
              type: integer
    """
    item = next((item for item in items if item['id'] == item_id), None)
    
    if item is None:
        return jsonify({
            "error": "Not Found",
            "message": f"Item with ID {item_id} not found",
            "status": 404
        }), 404
    
    return jsonify(item), 200


@app.route('/api/items', methods=['POST'])
def create_item():
    """
    Create a new item
    ---
    tags:
      - Items
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - name
            - category
            - quantity
          properties:
            name:
              type: string
              example: Petri Dish
            category:
              type: string
              example: Glassware
            quantity:
              type: integer
              example: 50
    responses:
      201:
        description: Item created successfully
        schema:
          type: object
          properties:
            message:
              type: string
            item:
              type: object
      400:
        description: Invalid request data
        schema:
          type: object
          properties:
            error:
              type: string
            message:
              type: string
            status:
              type: integer
    """
    global next_id
    
    if not request.json:
        return jsonify({
            "error": "Bad Request",
            "message": "Request must be JSON",
            "status": 400
        }), 400
    
    required_fields = ['name', 'category', 'quantity']
    for field in required_fields:
        if field not in request.json:
            return jsonify({
                "error": "Bad Request",
                "message": f"Missing required field: {field}",
                "status": 400
            }), 400
    
    # Validate quantity is a non-negative integer
    try:
        quantity = int(request.json['quantity'])
        if quantity < 0:
            return jsonify({
                "error": "Bad Request",
                "message": "Quantity must be a non-negative integer",
                "status": 400
            }), 400
    except (ValueError, TypeError):
        return jsonify({
            "error": "Bad Request",
            "message": "Quantity must be a valid integer",
            "status": 400
        }), 400
    
    new_item = {
        "id": next_id,
        "name": request.json['name'],
        "category": request.json['category'],
        "quantity": quantity,
        "created_at": datetime.now().isoformat()
    }
    
    items.append(new_item)
    next_id += 1
    
    return jsonify({
        "message": "Item created successfully",
        "item": new_item
    }), 201


@app.route('/api/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    """
    Update an existing item
    ---
    tags:
      - Items
    parameters:
      - name: item_id
        in: path
        type: integer
        required: true
        description: ID of the item to update
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
            category:
              type: string
            quantity:
              type: integer
    responses:
      200:
        description: Item updated successfully
        schema:
          type: object
          properties:
            message:
              type: string
            item:
              type: object
      404:
        description: Item not found
      400:
        description: Invalid request data
    """
    if not request.json:
        return jsonify({
            "error": "Bad Request",
            "message": "Request must be JSON",
            "status": 400
        }), 400
    
    item = next((item for item in items if item['id'] == item_id), None)
    
    if item is None:
        return jsonify({
            "error": "Not Found",
            "message": f"Item with ID {item_id} not found",
            "status": 404
        }), 404
    
    # Update only provided fields
    if 'name' in request.json:
        item['name'] = request.json['name']
    if 'category' in request.json:
        item['category'] = request.json['category']
    if 'quantity' in request.json:
        # Validate quantity is a non-negative integer
        try:
            quantity = int(request.json['quantity'])
            if quantity < 0:
                return jsonify({
                    "error": "Bad Request",
                    "message": "Quantity must be a non-negative integer",
                    "status": 400
                }), 400
            item['quantity'] = quantity
        except (ValueError, TypeError):
            return jsonify({
                "error": "Bad Request",
                "message": "Quantity must be a valid integer",
                "status": 400
            }), 400
    
    return jsonify({
        "message": "Item updated successfully",
        "item": item
    }), 200


@app.route('/api/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    """
    Delete an item
    ---
    tags:
      - Items
    parameters:
      - name: item_id
        in: path
        type: integer
        required: true
        description: ID of the item to delete
    responses:
      200:
        description: Item deleted successfully
        schema:
          type: object
          properties:
            message:
              type: string
            item:
              type: object
      404:
        description: Item not found
    """
    global items
    
    item = next((item for item in items if item['id'] == item_id), None)
    
    if item is None:
        return jsonify({
            "error": "Not Found",
            "message": f"Item with ID {item_id} not found",
            "status": 404
        }), 404
    
    items = [i for i in items if i['id'] != item_id]
    
    return jsonify({
        "message": "Item deleted successfully",
        "item": item
    }), 200


if __name__ == '__main__':
    # Note: Debug mode is enabled for development only
    # For production deployment, set debug=False and use a production WSGI server
    import os
    debug_mode = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
