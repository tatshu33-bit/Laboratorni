from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import os
from functools import wraps
from datetime import datetime
import database as db
from flasgger import Swagger, swag_from

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Configure Swagger/OpenAPI documentation for REST API
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
        "description": "REST API for laboratory store management system (integrated with Lab 4)",
        "version": "2.0.0",
        "contact": {
            "name": "API Support",
            "email": "support@laboratorni.com"
        }
    },
    "basePath": "/",
    "schemes": ["http", "https"],
}

swagger = Swagger(app, config=swagger_config, template=swagger_template)

# Initialize database on startup
db.init_db()
db.seed_initial_data()

# Admin credentials (in production, use proper authentication)
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'admin123'


def admin_required(f):
    """Decorator to require admin authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('is_admin'):
            flash('Необхідна авторизація адміністратора', 'error')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
def index():
    """Головна сторінка"""
    products = db.get_all_products()
    featured_products = products[:3] if products else []
    return render_template('index.html', products=featured_products)


@app.route('/about')
def about():
    """Сторінка Про нас"""
    return render_template('about.html')


@app.route('/catalog')
def catalog():
    """Сторінка каталогу товарів"""
    products = db.get_all_products()
    return render_template('catalog.html', products=products)


@app.route('/cart')
def cart():
    """Сторінка кошика"""
    cart_items = session.get('cart', [])
    cart_products = []
    total = 0
    
    for item in cart_items:
        product = db.get_product_by_id(item['id'])
        if product:
            cart_product = dict(product)
            cart_product['quantity'] = item['quantity']
            cart_product['subtotal'] = product['price'] * item['quantity']
            cart_products.append(cart_product)
            total += cart_product['subtotal']
    
    return render_template('cart.html', cart_products=cart_products, total=total)


@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    """Додати товар до кошика"""
    product = db.get_product_by_id(product_id)
    
    if not product:
        flash('Товар не знайдено', 'error')
        return redirect(request.referrer or url_for('index'))
    
    cart = session.get('cart', [])
    
    # Check if product already in cart
    cart_item = next((item for item in cart if item['id'] == product_id), None)
    
    if cart_item:
        cart_item['quantity'] += 1
    else:
        cart.append({'id': product_id, 'quantity': 1})
    
    session['cart'] = cart
    flash(f'"{product["name"]}" додано до кошика', 'success')
    
    return redirect(request.referrer or url_for('index'))


@app.route('/remove_from_cart/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    """Видалити товар з кошика"""
    cart = session.get('cart', [])
    cart = [item for item in cart if item['id'] != product_id]
    session['cart'] = cart
    flash('Товар видалено з кошика', 'info')
    return redirect(url_for('cart'))


@app.route('/update_cart/<int:product_id>', methods=['POST'])
def update_cart(product_id):
    """Оновити кількість товару в кошику"""
    quantity = int(request.form.get('quantity', 1))
    
    if quantity < 1:
        return redirect(url_for('cart'))
    
    cart = session.get('cart', [])
    cart_item = next((item for item in cart if item['id'] == product_id), None)
    
    if cart_item:
        cart_item['quantity'] = quantity
        session['cart'] = cart
        flash('Кошик оновлено', 'success')
    
    return redirect(url_for('cart'))


@app.route('/checkout')
def checkout():
    """
    Сторінка оформлення замовлення.
    Відображає форму для введення контактної інформації та підсумок замовлення.
    """
    cart_items = session.get('cart', [])
    
    # Redirect to cart if empty
    if not cart_items:
        flash('Ваш кошик порожній', 'error')
        return redirect(url_for('cart'))
    
    # Prepare cart products for display
    cart_products = []
    total = 0
    
    for item in cart_items:
        product = db.get_product_by_id(item['id'])
        if product:
            cart_product = dict(product)
            cart_product['quantity'] = item['quantity']
            cart_product['subtotal'] = product['price'] * item['quantity']
            cart_products.append(cart_product)
            total += cart_product['subtotal']
    
    return render_template('checkout.html', cart_products=cart_products, total=total)


@app.route('/place_order', methods=['POST'])
def place_order():
    """
    Обробка оформлення замовлення.
    Створює або оновлює клієнта, створює замовлення з товарами,
    очищає кошик та перенаправляє на сторінку підтвердження.
    """
    cart_items = session.get('cart', [])
    
    # Validate cart is not empty
    if not cart_items:
        flash('Ваш кошик порожній', 'error')
        return redirect(url_for('cart'))
    
    # Get form data
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    phone = request.form.get('phone', '').strip()
    address = request.form.get('address', '').strip()
    
    # Validate required fields
    if not name or not email or not phone or not address:
        flash('Будь ласка, заповніть всі обов\'язкові поля', 'error')
        return redirect(url_for('checkout'))
    
    try:
        # Get or create client
        client_id = db.get_or_create_client(name, email, phone, address)
        
        # Prepare order items
        order_items = []
        for item in cart_items:
            product = db.get_product_by_id(item['id'])
            if product:
                # Each item is (product_id, quantity, price)
                order_items.append((product['id'], item['quantity'], product['price']))
        
        # Create order
        order_id = db.create_order(client_id, order_items)
        
        # Clear cart
        session.pop('cart', None)
        
        # Redirect to confirmation page
        flash('Замовлення успішно оформлено!', 'success')
        return redirect(url_for('order_confirmation', order_id=order_id))
        
    except Exception as e:
        flash('Помилка при оформленні замовлення. Спробуйте ще раз.', 'error')
        return redirect(url_for('checkout'))


@app.route('/order_confirmation/<int:order_id>')
def order_confirmation(order_id):
    """
    Сторінка підтвердження замовлення.
    Відображає деталі оформленого замовлення.
    """
    order = db.get_order_by_id(order_id)
    
    if not order:
        flash('Замовлення не знайдено', 'error')
        return redirect(url_for('index'))
    
    items = db.get_order_items(order_id)
    
    return render_template('order_confirmation.html',
                         order_id=order_id,
                         order_date=order['created_at'],
                         total=order['total_amount'],
                         order_items=items,
                         client_name=order['client_name'] if order['client_name'] else 'N/A',
                         client_email=order['client_email'] if order['client_email'] else 'N/A',
                         client_phone=order['client_phone'] if order['client_phone'] else 'N/A',
                         client_address=order['client_address'] if order['client_address'] else 'N/A')


@app.route('/reviews')
def reviews():
    """Сторінка відгуків"""
    feedback = db.get_all_feedback()
    return render_template('reviews.html', reviews=feedback)


@app.route('/submit_review', methods=['POST'])
def submit_review():
    """Додати новий відгук"""
    author = request.form.get('author', '').strip()
    email = request.form.get('email', '').strip()
    rating = request.form.get('rating', type=int)
    text = request.form.get('text', '').strip()
    
    if not author or not rating or not text:
        flash('Будь ласка, заповніть всі обов\'язкові поля', 'error')
        return redirect(url_for('reviews'))
    
    if rating < 1 or rating > 5:
        flash('Оцінка повинна бути від 1 до 5', 'error')
        return redirect(url_for('reviews'))
    
    try:
        db.create_feedback(author, email, rating, text)
        flash('Дякуємо за ваш відгук!', 'success')
    except Exception as e:
        flash('Помилка при збереженні відгуку', 'error')
    
    return redirect(url_for('reviews'))


@app.route('/contacts')
def contacts():
    """Сторінка контактів"""
    return render_template('contacts.html')


@app.route('/delivery')
def delivery():
    """Сторінка інформації про доставку"""
    return render_template('delivery.html')


# Admin Panel Routes

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin login page"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['is_admin'] = True
            flash('Ви успішно увійшли як адміністратор', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Невірне ім\'я користувача або пароль', 'error')
    
    return render_template('admin/login.html')


@app.route('/admin/logout')
def admin_logout():
    """Admin logout"""
    session.pop('is_admin', None)
    flash('Ви вийшли з адмін-панелі', 'info')
    return redirect(url_for('index'))


@app.route('/admin')
@admin_required
def admin_dashboard():
    """Admin dashboard"""
    feedback_count = len(db.get_all_feedback())
    products_count = len(db.get_all_products())
    orders_count = len(db.get_all_orders())
    clients_count = len(db.get_all_clients())
    
    return render_template('admin/dashboard.html',
                         feedback_count=feedback_count,
                         products_count=products_count,
                         orders_count=orders_count,
                         clients_count=clients_count)


# Feedback Management
@app.route('/admin/feedback')
@admin_required
def admin_feedback():
    """List all feedback"""
    feedback = db.get_all_feedback()
    return render_template('admin/feedback.html', feedback=feedback)


@app.route('/admin/feedback/delete/<int:feedback_id>', methods=['POST'])
@admin_required
def admin_delete_feedback(feedback_id):
    """Delete feedback"""
    try:
        db.delete_feedback(feedback_id)
        flash('Відгук видалено', 'success')
    except Exception as e:
        flash('Помилка при видаленні відгуку', 'error')
    
    return redirect(url_for('admin_feedback'))


# Products Management
@app.route('/admin/products')
@admin_required
def admin_products():
    """List all products"""
    products = db.get_all_products()
    return render_template('admin/products.html', products=products)


@app.route('/admin/products/add', methods=['GET', 'POST'])
@admin_required
def admin_add_product():
    """Add new product"""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        category = request.form.get('category', '').strip()
        price = request.form.get('price', type=float)
        image = request.form.get('image', '').strip()
        description = request.form.get('description', '').strip()
        stock = request.form.get('stock', type=int, default=0)
        
        if not name or not category or price is None:
            flash('Будь ласка, заповніть всі обов\'язкові поля', 'error')
        else:
            try:
                db.create_product(name, category, price, image, description, stock)
                flash('Товар додано', 'success')
                return redirect(url_for('admin_products'))
            except Exception as e:
                flash('Помилка при додаванні товару', 'error')
    
    return render_template('admin/product_form.html', product=None)


@app.route('/admin/products/edit/<int:product_id>', methods=['GET', 'POST'])
@admin_required
def admin_edit_product(product_id):
    """Edit product"""
    product = db.get_product_by_id(product_id)
    
    if not product:
        flash('Товар не знайдено', 'error')
        return redirect(url_for('admin_products'))
    
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        category = request.form.get('category', '').strip()
        price = request.form.get('price', type=float)
        image = request.form.get('image', '').strip()
        description = request.form.get('description', '').strip()
        stock = request.form.get('stock', type=int, default=0)
        
        if not name or not category or price is None:
            flash('Будь ласка, заповніть всі обов\'язкові поля', 'error')
        else:
            try:
                db.update_product(product_id, name, category, price, image, description, stock)
                flash('Товар оновлено', 'success')
                return redirect(url_for('admin_products'))
            except Exception as e:
                flash('Помилка при оновленні товару', 'error')
    
    return render_template('admin/product_form.html', product=product)


@app.route('/admin/products/delete/<int:product_id>', methods=['POST'])
@admin_required
def admin_delete_product(product_id):
    """Delete product"""
    try:
        db.delete_product(product_id)
        flash('Товар видалено', 'success')
    except Exception as e:
        flash('Помилка при видаленні товару', 'error')
    
    return redirect(url_for('admin_products'))


# Orders Management
@app.route('/admin/orders')
@admin_required
def admin_orders():
    """List all orders"""
    orders = db.get_all_orders()
    return render_template('admin/orders.html', orders=orders)


@app.route('/admin/orders/<int:order_id>')
@admin_required
def admin_order_detail(order_id):
    """View order details"""
    order = db.get_order_by_id(order_id)
    if not order:
        flash('Замовлення не знайдено', 'error')
        return redirect(url_for('admin_orders'))
    
    items = db.get_order_items(order_id)
    return render_template('admin/order_detail.html', order=order, items=items)


@app.route('/admin/orders/<int:order_id>/status', methods=['POST'])
@admin_required
def admin_update_order_status(order_id):
    """Update order status"""
    status = request.form.get('status')
    
    if status not in ['pending', 'processing', 'shipped', 'delivered', 'cancelled']:
        flash('Невірний статус', 'error')
    else:
        try:
            db.update_order_status(order_id, status)
            flash('Статус замовлення оновлено', 'success')
        except Exception as e:
            flash('Помилка при оновленні статусу', 'error')
    
    return redirect(url_for('admin_order_detail', order_id=order_id))


@app.route('/admin/orders/delete/<int:order_id>', methods=['POST'])
@admin_required
def admin_delete_order(order_id):
    """Delete order"""
    try:
        db.delete_order(order_id)
        flash('Замовлення видалено', 'success')
    except Exception as e:
        flash('Помилка при видаленні замовлення', 'error')
    
    return redirect(url_for('admin_orders'))


# Clients Management
@app.route('/admin/clients')
@admin_required
def admin_clients():
    """List all clients"""
    clients = db.get_all_clients()
    return render_template('admin/clients.html', clients=clients)


@app.route('/admin/clients/add', methods=['GET', 'POST'])
@admin_required
def admin_add_client():
    """Add new client"""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        address = request.form.get('address', '').strip()
        
        if not name or not email:
            flash('Будь ласка, заповніть всі обов\'язкові поля', 'error')
        else:
            try:
                db.create_client(name, email, phone, address)
                flash('Клієнта додано', 'success')
                return redirect(url_for('admin_clients'))
            except Exception as e:
                flash('Помилка при додаванні клієнта (можливо, email вже використовується)', 'error')
    
    return render_template('admin/client_form.html', client=None)


@app.route('/admin/clients/edit/<int:client_id>', methods=['GET', 'POST'])
@admin_required
def admin_edit_client(client_id):
    """Edit client"""
    client = db.get_client_by_id(client_id)
    
    if not client:
        flash('Клієнта не знайдено', 'error')
        return redirect(url_for('admin_clients'))
    
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        address = request.form.get('address', '').strip()
        
        if not name or not email:
            flash('Будь ласка, заповніть всі обов\'язкові поля', 'error')
        else:
            try:
                db.update_client(client_id, name, email, phone, address)
                flash('Клієнта оновлено', 'success')
                return redirect(url_for('admin_clients'))
            except Exception as e:
                flash('Помилка при оновленні клієнта', 'error')
    
    return render_template('admin/client_form.html', client=client)


@app.route('/admin/clients/delete/<int:client_id>', methods=['POST'])
@admin_required
def admin_delete_client(client_id):
    """Delete client"""
    try:
        db.delete_client(client_id)
        flash('Клієнта видалено', 'success')
    except Exception as e:
        flash('Помилка при видаленні клієнта', 'error')
    
    return redirect(url_for('admin_clients'))


# ============================================================================
# REST API ENDPOINTS (Lab 5 Integration)
# ============================================================================

@app.errorhandler(404)
def api_not_found(error):
    """Handle 404 errors for API requests"""
    if request.path.startswith('/api/'):
        return jsonify({
            "error": "Not Found",
            "message": "The requested resource was not found",
            "status": 404
        }), 404
    # For non-API routes, use default error handling
    return error


@app.errorhandler(400)
def api_bad_request(error):
    """Handle 400 errors for API requests"""
    if request.path.startswith('/api/'):
        return jsonify({
            "error": "Bad Request",
            "message": str(error),
            "status": 400
        }), 400
    return error


@app.errorhandler(500)
def api_internal_error(error):
    """Handle 500 errors for API requests"""
    if request.path.startswith('/api/'):
        return jsonify({
            "error": "Internal Server Error",
            "message": "An unexpected error occurred",
            "status": 500
        }), 500
    return error


@app.route('/api/health', methods=['GET'])
def api_health_check():
    """
    Health check endpoint for monitoring API status
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
            version:
              type: string
              example: 2.0.0
    """
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0"
    }), 200


@app.route('/api/products', methods=['GET'])
def api_get_products():
    """
    Get all products from the store
    ---
    tags:
      - Products
    parameters:
      - name: category
        in: query
        type: string
        required: false
        description: Filter products by category
    responses:
      200:
        description: List of products
        schema:
          type: object
          properties:
            count:
              type: integer
            products:
              type: array
              items:
                type: object
    """
    products = db.get_all_products()
    category = request.args.get('category')
    
    if category:
        products = [p for p in products if p['category'].lower() == category.lower()]
    
    # Convert to serializable format
    products_list = []
    for p in products:
        products_list.append({
            'id': p['id'],
            'name': p['name'],
            'category': p['category'],
            'price': float(p['price']),
            'description': p['description'],
            'stock': p['stock'],
            'image': p['image'],
            'created_at': p['created_at']
        })
    
    return jsonify({
        "count": len(products_list),
        "products": products_list
    }), 200


@app.route('/api/products/<int:product_id>', methods=['GET'])
def api_get_product(product_id):
    """
    Get a specific product by ID
    ---
    tags:
      - Products
    parameters:
      - name: product_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Product details
      404:
        description: Product not found
    """
    product = db.get_product_by_id(product_id)
    
    if not product:
        return jsonify({
            "error": "Not Found",
            "message": f"Product with ID {product_id} not found",
            "status": 404
        }), 404
    
    return jsonify({
        'id': product['id'],
        'name': product['name'],
        'category': product['category'],
        'price': float(product['price']),
        'description': product['description'],
        'stock': product['stock'],
        'image': product['image'],
        'created_at': product['created_at']
    }), 200


@app.route('/api/products', methods=['POST'])
def api_create_product():
    """
    Create a new product (requires valid data)
    ---
    tags:
      - Products
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - name
            - category
            - price
            - stock
          properties:
            name:
              type: string
            category:
              type: string
            price:
              type: number
            stock:
              type: integer
            description:
              type: string
            image:
              type: string
    responses:
      201:
        description: Product created successfully
      400:
        description: Invalid request data
    """
    if not request.json:
        return jsonify({
            "error": "Bad Request",
            "message": "Request must be JSON",
            "status": 400
        }), 400
    
    required_fields = ['name', 'category', 'price', 'stock']
    for field in required_fields:
        if field not in request.json:
            return jsonify({
                "error": "Bad Request",
                "message": f"Missing required field: {field}",
                "status": 400
            }), 400
    
    # Validate price and stock
    try:
        price = float(request.json['price'])
        if price < 0:
            return jsonify({
                "error": "Bad Request",
                "message": "Price must be non-negative",
                "status": 400
            }), 400
    except (ValueError, TypeError):
        return jsonify({
            "error": "Bad Request",
            "message": "Price must be a valid number",
            "status": 400
        }), 400
    
    try:
        stock = int(request.json['stock'])
        if stock < 0:
            return jsonify({
                "error": "Bad Request",
                "message": "Stock must be non-negative",
                "status": 400
            }), 400
    except (ValueError, TypeError):
        return jsonify({
            "error": "Bad Request",
            "message": "Stock must be a valid integer",
            "status": 400
        }), 400
    
    product_id = db.create_product(
        name=request.json['name'],
        category=request.json['category'],
        price=price,
        image=request.json.get('image', ''),
        description=request.json.get('description', ''),
        stock=stock
    )
    
    product = db.get_product_by_id(product_id)
    
    return jsonify({
        "message": "Product created successfully",
        "product": {
            'id': product['id'],
            'name': product['name'],
            'category': product['category'],
            'price': float(product['price']),
            'description': product['description'],
            'stock': product['stock'],
            'image': product['image'],
            'created_at': product['created_at']
        }
    }), 201


@app.route('/api/products/<int:product_id>', methods=['PUT'])
def api_update_product(product_id):
    """
    Update an existing product
    ---
    tags:
      - Products
    parameters:
      - name: product_id
        in: path
        type: integer
        required: true
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
            price:
              type: number
            stock:
              type: integer
            description:
              type: string
            image:
              type: string
    responses:
      200:
        description: Product updated successfully
      404:
        description: Product not found
      400:
        description: Invalid request data
    """
    if not request.json:
        return jsonify({
            "error": "Bad Request",
            "message": "Request must be JSON",
            "status": 400
        }), 400
    
    product = db.get_product_by_id(product_id)
    if not product:
        return jsonify({
            "error": "Not Found",
            "message": f"Product with ID {product_id} not found",
            "status": 404
        }), 404
    
    # Validate numeric fields if provided
    if 'price' in request.json:
        try:
            price = float(request.json['price'])
            if price < 0:
                return jsonify({
                    "error": "Bad Request",
                    "message": "Price must be non-negative",
                    "status": 400
                }), 400
        except (ValueError, TypeError):
            return jsonify({
                "error": "Bad Request",
                "message": "Price must be a valid number",
                "status": 400
            }), 400
    
    if 'stock' in request.json:
        try:
            stock = int(request.json['stock'])
            if stock < 0:
                return jsonify({
                    "error": "Bad Request",
                    "message": "Stock must be non-negative",
                    "status": 400
                }), 400
        except (ValueError, TypeError):
            return jsonify({
                "error": "Bad Request",
                "message": "Stock must be a valid integer",
                "status": 400
            }), 400
    
    db.update_product(
        product_id=product_id,
        name=request.json.get('name', product['name']),
        category=request.json.get('category', product['category']),
        price=request.json.get('price', product['price']),
        image=request.json.get('image', product['image']),
        description=request.json.get('description', product['description']),
        stock=request.json.get('stock', product['stock'])
    )
    
    updated_product = db.get_product_by_id(product_id)
    
    return jsonify({
        "message": "Product updated successfully",
        "product": {
            'id': updated_product['id'],
            'name': updated_product['name'],
            'category': updated_product['category'],
            'price': float(updated_product['price']),
            'description': updated_product['description'],
            'stock': updated_product['stock'],
            'image': updated_product['image'],
            'created_at': updated_product['created_at']
        }
    }), 200


@app.route('/api/products/<int:product_id>', methods=['DELETE'])
def api_delete_product(product_id):
    """
    Delete a product
    ---
    tags:
      - Products
    parameters:
      - name: product_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Product deleted successfully
      404:
        description: Product not found
    """
    product = db.get_product_by_id(product_id)
    if not product:
        return jsonify({
            "error": "Not Found",
            "message": f"Product with ID {product_id} not found",
            "status": 404
        }), 404
    
    db.delete_product(product_id)
    
    return jsonify({
        "message": "Product deleted successfully",
        "product": {
            'id': product['id'],
            'name': product['name']
        }
    }), 200


@app.route('/api/feedback', methods=['GET'])
def api_get_feedback():
    """
    Get all feedback/reviews
    ---
    tags:
      - Feedback
    responses:
      200:
        description: List of feedback
        schema:
          type: object
          properties:
            count:
              type: integer
            feedback:
              type: array
    """
    feedback = db.get_all_feedback()
    
    feedback_list = []
    for f in feedback:
        feedback_list.append({
            'id': f['id'],
            'author': f['author'],
            'email': f['email'],
            'rating': f['rating'],
            'text': f['text'],
            'date': f['date']
        })
    
    return jsonify({
        "count": len(feedback_list),
        "feedback": feedback_list
    }), 200


@app.route('/api/feedback', methods=['POST'])
def api_create_feedback():
    """
    Submit new feedback/review
    ---
    tags:
      - Feedback
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - author
            - email
            - rating
            - text
          properties:
            author:
              type: string
            email:
              type: string
            rating:
              type: integer
              minimum: 1
              maximum: 5
            text:
              type: string
    responses:
      201:
        description: Feedback submitted successfully
      400:
        description: Invalid request data
    """
    if not request.json:
        return jsonify({
            "error": "Bad Request",
            "message": "Request must be JSON",
            "status": 400
        }), 400
    
    required_fields = ['author', 'email', 'rating', 'text']
    for field in required_fields:
        if field not in request.json:
            return jsonify({
                "error": "Bad Request",
                "message": f"Missing required field: {field}",
                "status": 400
            }), 400
    
    # Validate rating
    try:
        rating = int(request.json['rating'])
        if rating < 1 or rating > 5:
            return jsonify({
                "error": "Bad Request",
                "message": "Rating must be between 1 and 5",
                "status": 400
            }), 400
    except (ValueError, TypeError):
        return jsonify({
            "error": "Bad Request",
            "message": "Rating must be a valid integer",
            "status": 400
        }), 400
    
    feedback_id = db.create_feedback(
        author=request.json['author'],
        email=request.json['email'],
        rating=rating,
        text=request.json['text']
    )
    
    feedback = db.get_feedback_by_id(feedback_id)
    
    return jsonify({
        "message": "Feedback submitted successfully",
        "feedback": {
            'id': feedback['id'],
            'author': feedback['author'],
            'email': feedback['email'],
            'rating': feedback['rating'],
            'text': feedback['text'],
            'date': feedback['date']
        }
    }), 201


@app.route('/api/orders', methods=['GET'])
def api_get_orders():
    """
    Get all orders
    ---
    tags:
      - Orders
    parameters:
      - name: status
        in: query
        type: string
        required: false
        description: Filter orders by status
    responses:
      200:
        description: List of orders
    """
    orders = db.get_all_orders()
    status_filter = request.args.get('status')
    
    if status_filter:
        orders = [o for o in orders if o['status'] == status_filter]
    
    orders_list = []
    for o in orders:
        orders_list.append({
            'id': o['id'],
            'client_id': o['client_id'],
            'total_amount': float(o['total_amount']),
            'status': o['status'],
            'created_at': o['created_at'],
            'updated_at': o['updated_at']
        })
    
    return jsonify({
        "count": len(orders_list),
        "orders": orders_list
    }), 200


@app.route('/api/orders/<int:order_id>', methods=['GET'])
def api_get_order(order_id):
    """
    Get specific order details
    ---
    tags:
      - Orders
    parameters:
      - name: order_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Order details
      404:
        description: Order not found
    """
    order = db.get_order_by_id(order_id)
    
    if not order:
        return jsonify({
            "error": "Not Found",
            "message": f"Order with ID {order_id} not found",
            "status": 404
        }), 404
    
    items = db.get_order_items(order_id)
    
    return jsonify({
        'id': order['id'],
        'client_id': order['client_id'],
        'total_amount': float(order['total_amount']),
        'status': order['status'],
        'created_at': order['created_at'],
        'updated_at': order['updated_at'],
        'items': [{
            'product_id': item['product_id'],
            'product_name': item['product_name'],
            'quantity': item['quantity'],
            'price': float(item['price'])
        } for item in items]
    }), 200


if __name__ == '__main__':
    # Note: Debug mode should be disabled in production
    # Set FLASK_ENV=production in production environment
    debug_mode = os.environ.get('FLASK_ENV') != 'production'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
