from flask import Flask, render_template, request, redirect, url_for, session, flash
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Sample products data (clothing items)
PRODUCTS = [
    {
        'id': 1,
        'name': 'Класична сорочка',
        'category': 'Сорочки',
        'price': 899.00,
        'image': 'shirt1.jpg',
        'description': 'Елегантна білa сорочка для офісу'
    },
    {
        'id': 2,
        'name': 'Джинси Slim Fit',
        'category': 'Джинси',
        'price': 1299.00,
        'image': 'jeans1.jpg',
        'description': 'Стильні сині джинси вузького крою'
    },
    {
        'id': 3,
        'name': 'Светр в`язаний',
        'category': 'Светри',
        'price': 1099.00,
        'image': 'sweater1.jpg',
        'description': 'Теплий светр для холодної погоди'
    },
    {
        'id': 4,
        'name': 'Куртка шкіряна',
        'category': 'Куртки',
        'price': 3499.00,
        'image': 'jacket1.jpg',
        'description': 'Стильна шкіряна куртка'
    },
    {
        'id': 5,
        'name': 'Спортивний костюм',
        'category': 'Спортивний одяг',
        'price': 1599.00,
        'image': 'sportswear1.jpg',
        'description': 'Комфортний костюм для тренувань'
    },
    {
        'id': 6,
        'name': 'Плаття літнє',
        'category': 'Плаття',
        'price': 999.00,
        'image': 'dress1.jpg',
        'description': 'Легке літнє плаття'
    }
]

# Sample reviews data
REVIEWS = [
    {
        'id': 1,
        'author': 'Олена Петренко',
        'rating': 5,
        'text': 'Чудова якість одягу! Все підійшло ідеально. Обов\'язково буду замовляти ще.',
        'date': '15.11.2024'
    },
    {
        'id': 2,
        'author': 'Андрій Коваленко',
        'rating': 5,
        'text': 'Швидка доставка, відмінний сервіс. Рекомендую!',
        'date': '10.11.2024'
    },
    {
        'id': 3,
        'author': 'Марія Сидоренко',
        'rating': 4,
        'text': 'Хороший магазин, великий вибір. Ціни трохи високі, але якість того варта.',
        'date': '05.11.2024'
    }
]


@app.route('/')
def index():
    """Головна сторінка"""
    featured_products = PRODUCTS[:3]
    return render_template('index.html', products=featured_products)


@app.route('/about')
def about():
    """Сторінка Про нас"""
    return render_template('about.html')


@app.route('/catalog')
def catalog():
    """Сторінка каталогу товарів"""
    return render_template('catalog.html', products=PRODUCTS)


@app.route('/cart')
def cart():
    """Сторінка кошика"""
    cart_items = session.get('cart', [])
    cart_products = []
    total = 0
    
    for item in cart_items:
        product = next((p for p in PRODUCTS if p['id'] == item['id']), None)
        if product:
            cart_product = product.copy()
            cart_product['quantity'] = item['quantity']
            cart_product['subtotal'] = product['price'] * item['quantity']
            cart_products.append(cart_product)
            total += cart_product['subtotal']
    
    return render_template('cart.html', cart_products=cart_products, total=total)


@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    """Додати товар до кошика"""
    product = next((p for p in PRODUCTS if p['id'] == product_id), None)
    
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


@app.route('/reviews')
def reviews():
    """Сторінка відгуків"""
    return render_template('reviews.html', reviews=REVIEWS)


@app.route('/contacts')
def contacts():
    """Сторінка контактів"""
    return render_template('contacts.html')


@app.route('/delivery')
def delivery():
    """Сторінка інформації про доставку"""
    return render_template('delivery.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
