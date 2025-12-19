# API Test Report Template

## Project Information
- **Project Name**: Laboratorni REST API
- **Version**: 1.0.0
- **Test Date**: [Date]
- **Tester**: [Name]
- **Environment**: [Development/Staging/Production]

## Test Environment Setup
- **Server URL**: http://localhost:5000
- **Testing Tool**: Postman
- **Collection**: Laboratorni_API_Collection.postman_collection.json

## Test Summary

| Category | Total Tests | Passed | Failed | Pass Rate |
|----------|-------------|--------|--------|-----------|
| System Endpoints | 2 | - | - | -% |
| CRUD Operations | 9 | - | - | -% |
| **Total** | **11** | **-** | **-** | **-%** |

## Detailed Test Results

### 1. System Endpoints

#### 1.1 Root Endpoint Test
- **Endpoint**: `GET /`
- **Expected Response**: 200 OK
- **Response Body**:
  ```json
  {
    "message": "Welcome to Laboratorni REST API",
    "documentation": "/api/docs"
  }
  ```
- **Status**: [ ] Pass [ ] Fail
- **Notes**: 

#### 1.2 Health Check Test
- **Endpoint**: `GET /api/health`
- **Expected Response**: 200 OK
- **Response Body**:
  ```json
  {
    "status": "healthy",
    "timestamp": "[timestamp]",
    "version": "1.0.0"
  }
  ```
- **Status**: [ ] Pass [ ] Fail
- **Notes**: 

### 2. Item Management - CRUD Operations

#### 2.1 Get All Items
- **Endpoint**: `GET /api/items`
- **Expected Response**: 200 OK
- **Response Contains**: List of items with count
- **Status**: [ ] Pass [ ] Fail
- **Notes**: 

#### 2.2 Get Items by Category Filter
- **Endpoint**: `GET /api/items?category=Equipment`
- **Expected Response**: 200 OK
- **Response Contains**: Filtered items
- **Status**: [ ] Pass [ ] Fail
- **Notes**: 

#### 2.3 Get Item by ID (Success)
- **Endpoint**: `GET /api/items/1`
- **Expected Response**: 200 OK
- **Response Contains**: Single item object
- **Status**: [ ] Pass [ ] Fail
- **Notes**: 

#### 2.4 Get Non-Existent Item (404 Error)
- **Endpoint**: `GET /api/items/999`
- **Expected Response**: 404 Not Found
- **Response Body**:
  ```json
  {
    "error": "Not Found",
    "message": "Item with ID 999 not found",
    "status": 404
  }
  ```
- **Status**: [ ] Pass [ ] Fail
- **Notes**: 

#### 2.5 Create New Item (Success)
- **Endpoint**: `POST /api/items`
- **Request Body**:
  ```json
  {
    "name": "Petri Dish",
    "category": "Glassware",
    "quantity": 50
  }
  ```
- **Expected Response**: 201 Created
- **Response Contains**: Success message and created item
- **Status**: [ ] Pass [ ] Fail
- **Notes**: 

#### 2.6 Create Item with Missing Field (400 Error)
- **Endpoint**: `POST /api/items`
- **Request Body**:
  ```json
  {
    "name": "Incomplete Item",
    "category": "Equipment"
  }
  ```
- **Expected Response**: 400 Bad Request
- **Response Contains**: Error message about missing field
- **Status**: [ ] Pass [ ] Fail
- **Notes**: 

#### 2.7 Update Item (Success)
- **Endpoint**: `PUT /api/items/1`
- **Request Body**:
  ```json
  {
    "quantity": 8
  }
  ```
- **Expected Response**: 200 OK
- **Response Contains**: Success message and updated item
- **Status**: [ ] Pass [ ] Fail
- **Notes**: 

#### 2.8 Update Non-Existent Item (404 Error)
- **Endpoint**: `PUT /api/items/999`
- **Request Body**:
  ```json
  {
    "quantity": 10
  }
  ```
- **Expected Response**: 404 Not Found
- **Response Contains**: Error message
- **Status**: [ ] Pass [ ] Fail
- **Notes**: 

#### 2.9 Delete Item (Success)
- **Endpoint**: `DELETE /api/items/3`
- **Expected Response**: 200 OK
- **Response Contains**: Success message and deleted item
- **Status**: [ ] Pass [ ] Fail
- **Notes**: 

#### 2.10 Delete Non-Existent Item (404 Error)
- **Endpoint**: `DELETE /api/items/999`
- **Expected Response**: 404 Not Found
- **Response Contains**: Error message
- **Status**: [ ] Pass [ ] Fail
- **Notes**: 

### 3. API Documentation Tests

#### 3.1 Swagger UI Accessibility
- **Endpoint**: `GET /api/docs`
- **Expected**: Swagger UI loads successfully
- **Status**: [ ] Pass [ ] Fail
- **Notes**: 

#### 3.2 API Specification Availability
- **Endpoint**: `GET /apispec.json`
- **Expected**: Valid OpenAPI/Swagger JSON
- **Status**: [ ] Pass [ ] Fail
- **Notes**: 

## Error Handling Verification

### HTTP Status Codes
- [ ] 200 OK - Successful GET, PUT, DELETE
- [ ] 201 Created - Successful POST
- [ ] 400 Bad Request - Invalid data or missing fields
- [ ] 404 Not Found - Resource doesn't exist
- [ ] 500 Internal Server Error - Unexpected errors

### Error Response Format
All error responses follow consistent format:
```json
{
  "error": "[Error Type]",
  "message": "[Detailed message]",
  "status": [HTTP status code]
}
```
- **Status**: [ ] Pass [ ] Fail

## JSON Format Verification
- [ ] All requests accept JSON (Content-Type: application/json)
- [ ] All responses return JSON format
- [ ] Response structure is consistent
- [ ] Proper data types used (strings, integers, arrays, objects)

## Performance Notes
- **Average Response Time**: [ms]
- **Slowest Endpoint**: [endpoint]
- **Fastest Endpoint**: [endpoint]

## Issues Found

### Critical Issues
1. [Description]
   - **Severity**: Critical/High/Medium/Low
   - **Steps to Reproduce**: 
   - **Expected**: 
   - **Actual**: 

### Minor Issues
1. [Description]

## Recommendations
1. [Recommendation 1]
2. [Recommendation 2]

## Conclusion
- **Overall Test Status**: [ ] Pass [ ] Fail
- **API Ready for**: [ ] Development [ ] Testing [ ] Production
- **Comments**: 

## Sign-off
- **Tester Name**: ___________________
- **Date**: ___________________
- **Signature**: ___________________
