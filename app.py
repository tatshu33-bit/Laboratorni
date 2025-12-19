from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
from functools import wraps
import database as db

app = Flask(__name__)
app.secret_key = os.urandom(24)

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


if __name__ == '__main__':
    # Note: Debug mode should be disabled in production
    # Set FLASK_ENV=production in production environment
    debug_mode = os.environ.get('FLASK_ENV') != 'production'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
