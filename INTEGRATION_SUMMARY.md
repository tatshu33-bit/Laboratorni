# Lab 4 & Lab 5 Integration Summary

## Overview
This document describes the integration of Lab 4 (SQLite database with web application) and Lab 5 (REST API) into a unified system.

## Integration Approach

### Architecture
```
┌─────────────────────────────────────────────┐
│         Flask Application (app.py)          │
├─────────────────────────────────────────────┤
│                                             │
│  ┌──────────────┐      ┌──────────────┐   │
│  │ Web Routes   │      │ API Routes   │   │
│  │ (Templates)  │      │ (JSON)       │   │
│  └──────┬───────┘      └──────┬───────┘   │
│         │                     │            │
│         └──────────┬──────────┘            │
│                    │                       │
│         ┌──────────▼──────────┐           │
│         │   database.py       │           │
│         │  (Shared DB Layer)  │           │
│         └──────────┬──────────┘           │
│                    │                       │
│         ┌──────────▼──────────┐           │
│         │   SQLite Database   │           │
│         │     (store.db)      │           │
│         └─────────────────────┘           │
└─────────────────────────────────────────────┘
```

### Key Integration Points

1. **Shared Database Layer**: Both web routes and API routes use the same `database.py` module
2. **Single Flask App**: One application serves both HTML pages and JSON API responses
3. **Consistent Data**: Changes via web interface are immediately visible in API and vice versa
4. **Error Handling**: API-specific error handlers for clean JSON responses

## Components from Lab 4

### Database (database.py)
- SQLite connection management
- CRUD operations for all entities
- Table initialization and seeding

### Web Application
- E-commerce store interface
- Admin panel with authentication
- Session management
- HTML templates with Jinja2

### Entities
- **Products**: Store inventory
- **Clients**: Customer information
- **Orders**: Purchase orders with items
- **Feedback**: Customer reviews

## Components from Lab 5

### REST API Endpoints
- Product management API (CRUD)
- Feedback/reviews API
- Orders query API
- Health check endpoint

### API Features
- Swagger/OpenAPI documentation (Flasgger)
- JSON request/response format
- Input validation
- Consistent error responses

## Technical Details

### Dependencies
```
Flask==3.0.0        # Web framework (from both labs)
flasgger==0.9.7.1   # API documentation (Lab 5)
Werkzeug==3.0.3     # WSGI utilities (Lab 4)
Jinja2==3.1.2       # Template engine (Lab 4)
```

### File Structure
```
.
├── app.py                      # Integrated Flask application
├── database.py                 # Shared database layer (Lab 4)
├── requirements.txt            # Combined dependencies
├── store.db                    # SQLite database (auto-generated)
├── static/                     # CSS, JS (Lab 4)
│   ├── css/style.css
│   └── js/main.js
├── templates/                  # HTML templates (Lab 4)
│   ├── *.html                 # Public pages
│   └── admin/*.html           # Admin pages
├── LAB4_README.md             # Lab 4 documentation
└── README.md                  # Integrated documentation
```

## API Endpoints Added

### Products API
| Method | Endpoint | Description | Validation |
|--------|----------|-------------|------------|
| GET | `/api/products` | List products | Category filter |
| GET | `/api/products/<id>` | Get product | - |
| POST | `/api/products` | Create product | Required fields, non-negative price/stock |
| PUT | `/api/products/<id>` | Update product | Non-negative price/stock |
| DELETE | `/api/products/<id>` | Delete product | - |

### Feedback API
| Method | Endpoint | Description | Validation |
|--------|----------|-------------|------------|
| GET | `/api/feedback` | List feedback | - |
| POST | `/api/feedback` | Submit feedback | Rating 1-5, required fields |

### Orders API
| Method | Endpoint | Description | Validation |
|--------|----------|-------------|------------|
| GET | `/api/orders` | List orders | Status filter |
| GET | `/api/orders/<id>` | Get order details | - |

### System API
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check |
| GET | `/api/docs` | Swagger UI |
| GET | `/apispec.json` | OpenAPI spec |

## Testing

### Web Interface Testing
1. Start server: `python app.py`
2. Open browser: `http://localhost:5000`
3. Test features:
   - Browse catalog
   - Add items to cart
   - Submit reviews
   - Access admin panel (admin/admin123)

### API Testing
1. Health check:
   ```bash
   curl http://localhost:5000/api/health
   ```

2. Get products:
   ```bash
   curl http://localhost:5000/api/products
   ```

3. Create feedback:
   ```bash
   curl -X POST http://localhost:5000/api/feedback \
     -H "Content-Type: application/json" \
     -d '{"author":"Test","email":"test@test.com","rating":5,"text":"Great!"}'
   ```

4. View Swagger docs:
   - Open browser: `http://localhost:5000/api/docs`

## Integration Benefits

1. **Unified Data Model**: Single source of truth in SQLite database
2. **Dual Access**: Users can interact via web UI or programmatic API
3. **Admin + API**: Admins manage via web, developers integrate via API
4. **Documentation**: Swagger UI documents all API endpoints
5. **Validation**: Consistent validation across both interfaces

## Migration Notes

### Changes from Lab 4
- Added Flasgger dependency
- Imported `jsonify` from Flask
- Added API error handlers (conditional on request path)
- Added REST API route handlers
- No changes to existing web routes or templates

### Changes from Lab 5 Original
- Replaced in-memory storage with SQLite database
- Used Lab 4's database functions
- Mapped API endpoints to actual database entities
- Added validation for database constraints

## Future Enhancements

1. **Authentication**: Add API key or JWT authentication
2. **Rate Limiting**: Prevent API abuse
3. **CORS**: Enable cross-origin requests for frontend apps
4. **Pagination**: Add pagination for large result sets
5. **Filtering**: Enhanced filtering for all endpoints
6. **WebSocket**: Real-time updates for orders/inventory
7. **API Versioning**: Version API endpoints (e.g., /api/v1/)

## Conclusion

The integration successfully combines:
- ✅ Lab 4's database-driven web application
- ✅ Lab 5's RESTful API with documentation
- ✅ Shared database layer for data consistency
- ✅ 10+ API endpoints with full CRUD operations
- ✅ Swagger/OpenAPI documentation
- ✅ Input validation and error handling

The system is ready for both user interaction via web interface and programmatic access via REST API.

---
**Version**: 2.0.0  
**Date**: December 19, 2025  
**Status**: Complete ✅
