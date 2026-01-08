# API Usage Examples

Comprehensive examples for using the Laboratorni REST API.

## Base URL

```
http://localhost:5000/api
```

---

## Authentication

Most endpoints don't require authentication. Admin endpoints require login via the web interface.

---

## System Endpoints

### Health Check

Check if the API is running.

**Request:**
```bash
curl -X GET http://localhost:5000/api/health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-12-19T19:17:23.556530",
  "version": "2.0.0"
}
```

---

## Products API

### List All Products

Get all products with their details.

**Request:**
```bash
curl -X GET http://localhost:5000/api/products
```

**Response:**
```json
{
  "count": 6,
  "products": [
    {
      "id": 1,
      "name": "Класична сорочка",
      "category": "Сорочки",
      "price": 899.0,
      "description": "Елегантна біла сорочка для офісу",
      "stock": 20,
      "image": "shirt1.jpg",
      "created_at": "2025-12-19 19:08:46"
    }
  ]
}
```

### Filter by Category

Get products from a specific category.

**Request:**
```bash
curl -X GET "http://localhost:5000/api/products?category=Джинси"
```

**Response:**
```json
{
  "count": 1,
  "products": [
    {
      "id": 2,
      "name": "Джинси Slim Fit",
      "category": "Джинси",
      "price": 1299.0,
      "stock": 15
    }
  ]
}
```

### Get Specific Product

Get details of a single product by ID.

**Request:**
```bash
curl -X GET http://localhost:5000/api/products/1
```

**Response:**
```json
{
  "category": "Сорочки",
  "created_at": "2025-12-19 19:08:46",
  "description": "Елегантна біла сорочка для офісу",
  "id": 1,
  "image": "shirt1.jpg",
  "name": "Класична сорочка",
  "price": 899.0,
  "stock": 20
}
```

### Create Product (Admin)

Add a new product to the catalog.

**Request:**
```bash
curl -X POST http://localhost:5000/api/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Нова куртка",
    "category": "Куртки",
    "price": 2500.0,
    "description": "Стильна зимова куртка",
    "stock": 10,
    "image": "jacket_new.jpg"
  }'
```

**Response:**
```json
{
  "id": 7,
  "message": "Product created successfully"
}
```

### Update Product (Admin)

Update an existing product.

**Request:**
```bash
curl -X PUT http://localhost:5000/api/products/1 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Класична сорочка (оновлена)",
    "category": "Сорочки",
    "price": 950.0,
    "description": "Елегантна біла сорочка для офісу",
    "stock": 25,
    "image": "shirt1.jpg"
  }'
```

**Response:**
```json
{
  "message": "Product updated successfully"
}
```

### Delete Product (Admin)

Remove a product from the catalog.

**Request:**
```bash
curl -X DELETE http://localhost:5000/api/products/7
```

**Response:**
```json
{
  "message": "Product deleted successfully"
}
```

---

## Feedback API

### List All Feedback

Get all customer reviews.

**Request:**
```bash
curl -X GET http://localhost:5000/api/feedback
```

**Response:**
```json
{
  "count": 2,
  "feedback": [
    {
      "id": 1,
      "author": "Іван Петренко",
      "email": "ivan@example.com",
      "rating": 5,
      "text": "Чудовий магазин! Якість товарів на висоті.",
      "date": "2025-12-19 10:30:00"
    },
    {
      "id": 2,
      "author": "Марія Коваль",
      "email": "maria@example.com",
      "rating": 4,
      "text": "Дуже задоволена покупкою. Рекомендую!",
      "date": "2025-12-19 11:15:00"
    }
  ]
}
```

### Submit Feedback

Add a new customer review.

**Request:**
```bash
curl -X POST http://localhost:5000/api/feedback \
  -H "Content-Type: application/json" \
  -d '{
    "author": "Олександр Сидоренко",
    "email": "oleksandr@example.com",
    "rating": 5,
    "text": "Відмінний сервіс та швидка доставка!"
  }'
```

**Response:**
```json
{
  "id": 3,
  "message": "Feedback submitted successfully"
}
```

**Validation Rules:**
- `author`: Required, 2-50 characters, letters only
- `email`: Optional, valid email format
- `rating`: Required, integer 1-5
- `text`: Required, 10-1000 characters

---

## Orders API

### List All Orders

Get all orders with client information.

**Request:**
```bash
curl -X GET http://localhost:5000/api/orders
```

**Response:**
```json
{
  "count": 2,
  "orders": [
    {
      "id": 1,
      "client_id": 1,
      "client_name": "Петро Іваненко",
      "client_email": "petro@example.com",
      "total_amount": 2198.0,
      "status": "processing",
      "created_at": "2025-12-19 12:00:00",
      "updated_at": "2025-12-19 13:00:00"
    }
  ]
}
```

### Filter by Status

Get orders with specific status.

**Request:**
```bash
curl -X GET "http://localhost:5000/api/orders?status=delivered"
```

**Status values:**
- `pending` - Замовлення прийнято
- `processing` - Обробляється
- `shipped` - Відправлено
- `delivered` - Доставлено
- `cancelled` - Скасовано

### Get Order Details

Get detailed information about a specific order.

**Request:**
```bash
curl -X GET http://localhost:5000/api/orders/1
```

**Response:**
```json
{
  "order": {
    "id": 1,
    "client_id": 1,
    "client_name": "Петро Іваненко",
    "client_email": "petro@example.com",
    "client_phone": "+380671234567",
    "client_address": "м. Київ, вул. Хрещатик 1, кв. 10",
    "total_amount": 2198.0,
    "status": "processing",
    "created_at": "2025-12-19 12:00:00",
    "updated_at": "2025-12-19 13:00:00"
  },
  "items": [
    {
      "id": 1,
      "product_id": 1,
      "product_name": "Класична сорочка",
      "quantity": 1,
      "price": 899.0
    },
    {
      "id": 2,
      "product_id": 2,
      "product_name": "Джинси Slim Fit",
      "quantity": 1,
      "price": 1299.0
    }
  ]
}
```

---

## Error Handling

### Error Response Format

All errors return JSON with error details.

**400 Bad Request:**
```json
{
  "error": "Invalid request data",
  "message": "Price must be a positive number"
}
```

**404 Not Found:**
```json
{
  "error": "Not found",
  "message": "Product with id 999 not found"
}
```

**500 Internal Server Error:**
```json
{
  "error": "Internal server error",
  "message": "Database error occurred"
}
```

---

## Using with JavaScript

### Fetch API Example

```javascript
// Get all products
async function getProducts() {
  try {
    const response = await fetch('http://localhost:5000/api/products');
    const data = await response.json();
    console.log('Products:', data.products);
    return data.products;
  } catch (error) {
    console.error('Error fetching products:', error);
  }
}

// Submit feedback
async function submitFeedback(feedbackData) {
  try {
    const response = await fetch('http://localhost:5000/api/feedback', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(feedbackData)
    });
    
    const result = await response.json();
    console.log('Feedback submitted:', result);
    return result;
  } catch (error) {
    console.error('Error submitting feedback:', error);
  }
}

// Usage
getProducts();

submitFeedback({
  author: 'Тестовий користувач',
  email: 'test@example.com',
  rating: 5,
  text: 'Чудовий API для інтернет-магазину!'
});
```

### Axios Example

```javascript
const axios = require('axios');

const API_BASE_URL = 'http://localhost:5000/api';

// Get product by ID
axios.get(`${API_BASE_URL}/products/1`)
  .then(response => {
    console.log('Product:', response.data);
  })
  .catch(error => {
    console.error('Error:', error.response.data);
  });

// Create new product
axios.post(`${API_BASE_URL}/products`, {
  name: 'Тестовий товар',
  category: 'Тест',
  price: 100.0,
  description: 'Опис тестового товару',
  stock: 5,
  image: 'test.jpg'
})
  .then(response => {
    console.log('Product created:', response.data);
  })
  .catch(error => {
    console.error('Error:', error.response.data);
  });
```

---

## Using with Python

### requests Library Example

```python
import requests
import json

API_BASE_URL = 'http://localhost:5000/api'

# Get all products
def get_products():
    response = requests.get(f'{API_BASE_URL}/products')
    if response.status_code == 200:
        data = response.json()
        print(f"Found {data['count']} products")
        return data['products']
    else:
        print(f"Error: {response.status_code}")
        return None

# Filter products by category
def get_products_by_category(category):
    params = {'category': category}
    response = requests.get(f'{API_BASE_URL}/products', params=params)
    return response.json()

# Submit feedback
def submit_feedback(author, rating, text, email=None):
    data = {
        'author': author,
        'rating': rating,
        'text': text
    }
    if email:
        data['email'] = email
    
    response = requests.post(
        f'{API_BASE_URL}/feedback',
        json=data,
        headers={'Content-Type': 'application/json'}
    )
    
    if response.status_code == 201:
        print('Feedback submitted successfully')
        return response.json()
    else:
        print(f'Error: {response.json()}')
        return None

# Usage
products = get_products()
jeans = get_products_by_category('Джинси')
submit_feedback('Python User', 5, 'Great API!')
```

---

## Postman Collection

Import the `Laboratorni_API_Collection.postman_collection.json` file into Postman for pre-configured requests.

**Steps:**
1. Open Postman
2. Click "Import"
3. Select the JSON file
4. All endpoints will be available in the collection

---

## Rate Limiting

**Default:** 100 requests per minute per IP

If exceeded, you'll receive:
```json
{
  "error": "Rate limit exceeded",
  "message": "Too many requests. Please try again later."
}
```

---

## Interactive Documentation

Visit the Swagger UI for interactive API documentation:

```
http://localhost:5000/api/docs
```

Features:
- Try API calls directly from browser
- See request/response schemas
- View all available endpoints
- Test authentication

---

## Best Practices

### 1. Always Check Response Status

```javascript
const response = await fetch(url);
if (!response.ok) {
  throw new Error(`HTTP error! status: ${response.status}`);
}
```

### 2. Use Proper Error Handling

```python
try:
    response = requests.post(url, json=data)
    response.raise_for_status()
except requests.exceptions.HTTPError as e:
    print(f"HTTP Error: {e}")
except requests.exceptions.ConnectionError as e:
    print(f"Connection Error: {e}")
```

### 3. Validate Data Before Sending

```javascript
function validateFeedback(data) {
  if (!data.author || data.author.length < 2) {
    throw new Error('Author name too short');
  }
  if (data.rating < 1 || data.rating > 5) {
    throw new Error('Rating must be between 1 and 5');
  }
  if (!data.text || data.text.length < 10) {
    throw new Error('Feedback text too short');
  }
}
```

### 4. Use Environment Variables

```bash
# .env
API_BASE_URL=http://localhost:5000/api
API_TIMEOUT=30
```

---

## Support

For issues or questions:
- Check API documentation: `/api/docs`
- Review this guide
- Contact: info@shop.ua
