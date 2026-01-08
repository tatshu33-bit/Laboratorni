# Laboratorni - Integrated Laboratory Applications

This repository contains multiple laboratory projects integrated into a comprehensive learning platform.

## Projects Overview

### Lab 4 & 5: E-commerce Web Application with REST API (Python/Flask)
A full-stack web application with SQLite database backend and RESTful API.

**Features:**
- **E-commerce Store**: Product catalog, shopping cart, checkout
- **Admin Panel**: Full CRUD operations for products, orders, clients, and feedback
- **Database**: SQLite with proper schema and relationships
- **REST API**: 10+ RESTful endpoints with Swagger documentation
- **User Features**: Browse products, submit reviews, place orders
- **Session Management**: Admin authentication

### Lab 6: Resource Manager (Node.js/Express)
A simple web application for managing learning resources with a modern interface.

**Features:**
- 📋 **Display Resources**: View all available resources in an organized list
- ➕ **Add Resources**: Submit new resources through an intuitive form
- ✅ **Validation**: Input validation for all form fields including URL validation
- 💬 **Feedback Messages**: Success and error messages for user actions
- 🎨 **Modern Design**: Clean, responsive UI with gradient backgrounds and smooth animations

---

## Lab 6: Resource Manager (Node.js/Express)

### Prerequisites
- Node.js (v14 or higher)
- npm (comes with Node.js)

### Installation

```bash
# Install Node.js dependencies
npm install
```

### Running the Application

```bash
npm start
```

The application will be available at: http://localhost:3000

### Resource Manager API Endpoints

#### GET /api/resources
Retrieves all resources.

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "Resource Name",
      "description": "Resource Description",
      "url": "https://example.com"
    }
  ]
}
```

#### POST /api/resources
Adds a new resource.

**Request Body:**
```json
{
  "name": "Resource Name",
  "description": "Resource Description",
  "url": "https://example.com"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Resource added successfully",
  "data": {
    "id": 4,
    "name": "Resource Name",
    "description": "Resource Description",
    "url": "https://example.com"
  }
}
```

### Usage

1. **View Resources**: The page automatically loads and displays all available resources
2. **Add New Resource**:
   - Fill in the resource name
   - Add a description
   - Provide a valid URL
   - Click "Add Resource" button
3. **Success/Error Messages**: Messages appear at the top of the page confirming actions or showing errors

---

## Lab 4 & 5: E-commerce Application (Python/Flask)

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

```bash
# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt
```

### Running the Application

```bash
python app.py
```

The application will be available at: http://localhost:5000

**Security Note:** By default, the API runs in debug mode for development. To run in production mode:
```bash
export FLASK_DEBUG=False
python app.py
```

### Application Endpoints

#### Web Interface (Templates)
- `GET /` - Home page with featured products
- `GET /catalog` - Product catalog
- `GET /cart` - Shopping cart
- `GET /reviews` - Customer reviews
- `GET /admin` - Admin dashboard (requires login)
- `GET /admin/products` - Manage products
- `GET /admin/orders` - Manage orders
- `GET /admin/clients` - Manage clients
- `GET /admin/feedback` - Manage feedback

#### REST API Endpoints

**System:**
- `GET /api/health` - Health check endpoint
- `GET /api/docs` - Interactive Swagger documentation

**Products API:**
- `GET /api/products` - Get all products (supports category filtering)
- `GET /api/products/<id>` - Get specific product by ID
- `POST /api/products` - Create a new product
- `PUT /api/products/<id>` - Update an existing product
- `DELETE /api/products/<id>` - Delete a product

**Feedback API:**
- `GET /api/feedback` - Get all feedback/reviews
- `POST /api/feedback` - Submit new feedback

**Orders API:**
- `GET /api/orders` - Get all orders (supports status filtering)
- `GET /api/orders/<id>` - Get specific order details with items

### API Documentation

Access the interactive Swagger documentation at: http://localhost:5000/api/docs

### Testing with Postman

Import the `Laboratorni_API_Collection.postman_collection.json` file into Postman to test all API endpoints.

---

## Project Structure

```
Laboratorni/
# Lab 6 - Resource Manager (Node.js)
├── server.js                  # Express server and API endpoints
├── package.json               # Node.js dependencies
├── public/                    # Frontend files
│   ├── index.html            # Main HTML page
│   ├── styles.css            # Styles and layout
│   └── app.js                # JavaScript for API interaction
│
# Lab 4 & 5 - E-commerce Application (Python)
├── app.py                     # Main Flask application
├── database.py                # Database layer
├── requirements.txt           # Python dependencies
├── templates/                 # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── catalog.html
│   ├── cart.html
│   ├── admin/                # Admin panel templates
│   └── ...
├── static/                    # Static assets
│   ├── css/style.css
│   └── js/main.js
├── Laboratorni_API_Collection.postman_collection.json
├── api_specification.json
├── api_specification.yaml
└── README.md                  # This file
```

## Technology Stack

### Lab 6 (Node.js)
- **Backend**: Node.js with Express
- **Frontend**: Vanilla HTML5, CSS3, and JavaScript
- **Data Storage**: In-memory storage

### Lab 4 & 5 (Python)
- **Flask 3.0.0** - Web framework
- **Flasgger 0.9.7.1** - Swagger/OpenAPI documentation
- **SQLite** - Database
- **Python 3.8+** - Programming language

## License

This project is part of laboratory coursework.
