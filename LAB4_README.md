# Lab 4 - SQLite Database and Admin Panel

## Overview
This project implements a complete web application with SQLite database backend, featuring:
- User feedback management
- Product catalog with inventory
- Order management with status tracking
- Client relationship management
- Full admin panel for CRUD operations

## Database Schema

### Tables
1. **feedback** - User reviews and ratings
   - Fields: id, author, email, rating (1-5), text, date
   
2. **products** - Store inventory
   - Fields: id, name, category, price, image, description, stock, created_at
   
3. **clients** - Customer information
   - Fields: id, name, email (unique), phone, address, created_at
   
4. **orders** - Customer orders
   - Fields: id, client_id (FK), total_amount, status, created_at, updated_at
   - Status options: pending, processing, shipped, delivered, cancelled
   
5. **order_items** - Order line items (junction table)
   - Fields: id, order_id (FK), product_id (FK), quantity, price

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Initialize the database:
```bash
python database.py
```

3. Run the application:
```bash
python app.py
```

The application will be available at http://localhost:5000

## Usage

### Public Site
- Browse products at `/catalog`
- View and submit reviews at `/reviews`
- Add products to cart and manage orders
- View information pages (about, delivery, contacts)

### Admin Panel
1. Navigate to `/admin`
2. Login with credentials:
   - Username: `admin`
   - Password: `admin123`

3. Available admin features:
   - **Dashboard**: Overview of all entities with statistics
   - **Feedback Management**: View and delete user reviews
   - **Products Management**: Full CRUD for products including stock management
   - **Orders Management**: View orders, update status, manage order lifecycle
   - **Clients Management**: Full CRUD for client information

### Order Status Workflow
```
pending → processing → shipped → delivered
                  ↓
              cancelled
```

## Features

### Level 1 Implementation
✅ SQLite database with proper schema
✅ Feedback table with CRUD operations
✅ Basic admin panel with authentication
✅ Store functionality (products, orders)
✅ Table relationships (orders ↔ products via order_items)
✅ Order status management
✅ Extended admin panel for all entities

### Level 2 Implementation
✅ Clients table integrated with domain
✅ Full CRUD operations for clients
✅ Admin panel functionality for clients
✅ Integration with orders system

## Technical Details

- **Framework**: Flask 3.0.0
- **Database**: SQLite 3
- **Authentication**: Session-based admin login
- **UI**: Responsive design with clean admin interface
- **Validation**: Form validation and database constraints
- **Security**: SQL injection protection via parameterized queries

## File Structure
```
.
├── app.py                      # Main Flask application
├── database.py                 # Database layer and CRUD operations
├── requirements.txt            # Python dependencies
├── store.db                    # SQLite database (auto-generated)
├── static/
│   ├── css/style.css          # Styles
│   └── js/main.js             # JavaScript
└── templates/
    ├── base.html              # Base template for public site
    ├── *.html                 # Public pages
    └── admin/
        ├── base.html          # Base template for admin
        └── *.html             # Admin pages
```

## Notes

- The database file (`store.db`) is excluded from version control via `.gitignore`
- Initial sample data is automatically seeded on first run
- Admin credentials should be changed in production environment
- Debug mode is enabled by default (disable in production)
