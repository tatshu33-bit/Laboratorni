import sqlite3
from datetime import datetime
import os

DATABASE_PATH = 'store.db'


def get_db_connection():
    """Create and return a database connection"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize the database with all required tables"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create feedback table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            author TEXT NOT NULL,
            email TEXT,
            rating INTEGER NOT NULL CHECK(rating >= 1 AND rating <= 5),
            text TEXT NOT NULL,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create products table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL CHECK(price >= 0),
            image TEXT,
            description TEXT,
            stock INTEGER DEFAULT 0 CHECK(stock >= 0),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create clients table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT,
            address TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create orders table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER,
            total_amount REAL NOT NULL CHECK(total_amount >= 0),
            status TEXT DEFAULT 'pending' CHECK(status IN ('pending', 'processing', 'shipped', 'delivered', 'cancelled')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (client_id) REFERENCES clients(id) ON DELETE SET NULL
        )
    ''')
    
    # Create order_items table (junction table for orders and products)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL CHECK(quantity > 0),
            price REAL NOT NULL CHECK(price >= 0),
            FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
            FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
        )
    ''')
    
    conn.commit()
    conn.close()


def seed_initial_data():
    """Seed the database with initial sample data"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if products already exist
    cursor.execute('SELECT COUNT(*) FROM products')
    if cursor.fetchone()[0] == 0:
        # Insert sample products
        products = [
            ('Класична сорочка', 'Сорочки', 899.00, 'shirt1.jpg', 'Елегантна біла сорочка для офісу', 20),
            ('Джинси Slim Fit', 'Джинси', 1299.00, 'jeans1.jpg', 'Стильні сині джинси вузького крою', 15),
            ('Светр в\'язаний', 'Светри', 1099.00, 'sweater1.jpg', 'Теплий светр для холодної погоди', 10),
            ('Куртка шкіряна', 'Куртки', 3499.00, 'jacket1.jpg', 'Стильна шкіряна куртка', 5),
            ('Спортивний костюм', 'Спортивний одяг', 1599.00, 'sportswear1.jpg', 'Комфортний костюм для тренувань', 12),
            ('Плаття літнє', 'Плаття', 999.00, 'dress1.jpg', 'Легке літнє плаття', 8)
        ]
        
        cursor.executemany(
            'INSERT INTO products (name, category, price, image, description, stock) VALUES (?, ?, ?, ?, ?, ?)',
            products
        )
    
    # Check if feedback already exists
    cursor.execute('SELECT COUNT(*) FROM feedback')
    if cursor.fetchone()[0] == 0:
        # Insert sample feedback
        feedbacks = [
            ('Олена Петренко', 'olena@example.com', 5, 'Чудова якість одягу! Все підійшло ідеально. Обов\'язково буду замовляти ще.'),
            ('Андрій Коваленко', 'andrii@example.com', 5, 'Швидка доставка, відмінний сервіс. Рекомендую!'),
            ('Марія Сидоренко', 'maria@example.com', 4, 'Хороший магазин, великий вибір. Ціни трохи високі, але якість того варта.')
        ]
        
        cursor.executemany(
            'INSERT INTO feedback (author, email, rating, text) VALUES (?, ?, ?, ?)',
            feedbacks
        )
    
    # Check if clients already exist
    cursor.execute('SELECT COUNT(*) FROM clients')
    if cursor.fetchone()[0] == 0:
        # Insert sample clients
        clients = [
            ('Олена Петренко', 'olena@example.com', '+380501234567', 'Київ, вул. Хрещатик 1'),
            ('Андрій Коваленко', 'andrii@example.com', '+380502345678', 'Львів, вул. Городоцька 20'),
            ('Марія Сидоренко', 'maria@example.com', '+380503456789', 'Одеса, вул. Дерибасівська 5')
        ]
        
        cursor.executemany(
            'INSERT INTO clients (name, email, phone, address) VALUES (?, ?, ?, ?)',
            clients
        )
    
    conn.commit()
    conn.close()


# Feedback CRUD operations
def get_all_feedback():
    """Get all feedback entries"""
    conn = get_db_connection()
    feedback = conn.execute('SELECT * FROM feedback ORDER BY date DESC').fetchall()
    conn.close()
    return feedback


def get_feedback_by_id(feedback_id):
    """Get a specific feedback entry by ID"""
    conn = get_db_connection()
    feedback = conn.execute('SELECT * FROM feedback WHERE id = ?', (feedback_id,)).fetchone()
    conn.close()
    return feedback


def create_feedback(author, email, rating, text):
    """Create a new feedback entry"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO feedback (author, email, rating, text) VALUES (?, ?, ?, ?)',
        (author, email, rating, text)
    )
    conn.commit()
    feedback_id = cursor.lastrowid
    conn.close()
    return feedback_id


def delete_feedback(feedback_id):
    """Delete a feedback entry"""
    conn = get_db_connection()
    conn.execute('DELETE FROM feedback WHERE id = ?', (feedback_id,))
    conn.commit()
    conn.close()


# Products CRUD operations
def get_all_products():
    """Get all products"""
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products ORDER BY name').fetchall()
    conn.close()
    return products


def get_product_by_id(product_id):
    """Get a specific product by ID"""
    conn = get_db_connection()
    product = conn.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()
    conn.close()
    return product


def create_product(name, category, price, image, description, stock=0):
    """Create a new product"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO products (name, category, price, image, description, stock) VALUES (?, ?, ?, ?, ?, ?)',
        (name, category, price, image, description, stock)
    )
    conn.commit()
    product_id = cursor.lastrowid
    conn.close()
    return product_id


def update_product(product_id, name, category, price, image, description, stock):
    """Update a product"""
    conn = get_db_connection()
    conn.execute(
        'UPDATE products SET name = ?, category = ?, price = ?, image = ?, description = ?, stock = ? WHERE id = ?',
        (name, category, price, image, description, stock, product_id)
    )
    conn.commit()
    conn.close()


def delete_product(product_id):
    """Delete a product"""
    conn = get_db_connection()
    conn.execute('DELETE FROM products WHERE id = ?', (product_id,))
    conn.commit()
    conn.close()


# Clients CRUD operations
def get_all_clients():
    """Get all clients"""
    conn = get_db_connection()
    clients = conn.execute('SELECT * FROM clients ORDER BY name').fetchall()
    conn.close()
    return clients


def get_client_by_id(client_id):
    """Get a specific client by ID"""
    conn = get_db_connection()
    client = conn.execute('SELECT * FROM clients WHERE id = ?', (client_id,)).fetchone()
    conn.close()
    return client


def create_client(name, email, phone, address):
    """Create a new client"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO clients (name, email, phone, address) VALUES (?, ?, ?, ?)',
        (name, email, phone, address)
    )
    conn.commit()
    client_id = cursor.lastrowid
    conn.close()
    return client_id


def update_client(client_id, name, email, phone, address):
    """Update a client"""
    conn = get_db_connection()
    conn.execute(
        'UPDATE clients SET name = ?, email = ?, phone = ?, address = ? WHERE id = ?',
        (name, email, phone, address, client_id)
    )
    conn.commit()
    conn.close()


def delete_client(client_id):
    """Delete a client"""
    conn = get_db_connection()
    conn.execute('DELETE FROM clients WHERE id = ?', (client_id,))
    conn.commit()
    conn.close()


# Orders CRUD operations
def get_all_orders():
    """Get all orders with client information"""
    conn = get_db_connection()
    orders = conn.execute('''
        SELECT o.*, c.name as client_name, c.email as client_email 
        FROM orders o
        LEFT JOIN clients c ON o.client_id = c.id
        ORDER BY o.created_at DESC
    ''').fetchall()
    conn.close()
    return orders


def get_order_by_id(order_id):
    """Get a specific order by ID with client information"""
    conn = get_db_connection()
    order = conn.execute('''
        SELECT o.*, c.name as client_name, c.email as client_email 
        FROM orders o
        LEFT JOIN clients c ON o.client_id = c.id
        WHERE o.id = ?
    ''', (order_id,)).fetchone()
    conn.close()
    return order


def get_order_items(order_id):
    """Get all items for a specific order"""
    conn = get_db_connection()
    items = conn.execute('''
        SELECT oi.*, p.name as product_name, p.image as product_image
        FROM order_items oi
        JOIN products p ON oi.product_id = p.id
        WHERE oi.order_id = ?
    ''', (order_id,)).fetchall()
    conn.close()
    return items


def create_order(client_id, items):
    """
    Create a new order with items
    items is a list of tuples: [(product_id, quantity, price), ...]
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Calculate total
    total_amount = sum(item[2] * item[1] for item in items)
    
    # Create order
    cursor.execute(
        'INSERT INTO orders (client_id, total_amount) VALUES (?, ?)',
        (client_id, total_amount)
    )
    order_id = cursor.lastrowid
    
    # Add order items
    for product_id, quantity, price in items:
        cursor.execute(
            'INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (?, ?, ?, ?)',
            (order_id, product_id, quantity, price)
        )
    
    conn.commit()
    conn.close()
    return order_id


def update_order_status(order_id, status):
    """Update the status of an order"""
    conn = get_db_connection()
    conn.execute(
        'UPDATE orders SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
        (status, order_id)
    )
    conn.commit()
    conn.close()


def delete_order(order_id):
    """Delete an order and its items"""
    conn = get_db_connection()
    conn.execute('DELETE FROM orders WHERE id = ?', (order_id,))
    conn.commit()
    conn.close()


if __name__ == '__main__':
    # Initialize database
    print("Initializing database...")
    init_db()
    print("Seeding initial data...")
    seed_initial_data()
    print("Database setup complete!")
