"""
Flask application with SQLite database
"""
import os
import sqlite3
from flask import Flask, jsonify, request, g

app = Flask(__name__)

# Configuration from environment variables
app.config['DATABASE'] = os.environ.get('DATABASE_PATH', '/app/data/app.db')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')


def get_db():
    """Get database connection"""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE'])
        db.row_factory = sqlite3.Row
    return db


@app.teardown_appcontext
def close_connection(exception):
    """Close database connection"""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def init_db():
    """Initialize the database"""
    with app.app_context():
        db = get_db()
        db.execute('''
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        db.commit()


@app.route('/')
def index():
    """Root endpoint"""
    return jsonify({
        'message': 'Flask SQLite Application',
        'status': 'running',
        'endpoints': {
            '/': 'This page',
            '/health': 'Health check endpoint',
            '/items': 'GET: List all items, POST: Create item',
            '/items/<id>': 'GET: Get item, PUT: Update item, DELETE: Delete item'
        }
    })


@app.route('/health')
def health():
    """Health check endpoint"""
    try:
        db = get_db()
        db.execute('SELECT 1').fetchone()
        return jsonify({'status': 'healthy', 'database': 'connected'}), 200
    except Exception as e:
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 503


@app.route('/items', methods=['GET', 'POST'])
def items():
    """List all items or create a new item"""
    db = get_db()
    
    if request.method == 'GET':
        cursor = db.execute('SELECT * FROM items ORDER BY created_at DESC')
        items = [dict(row) for row in cursor.fetchall()]
        return jsonify({'items': items})
    
    elif request.method == 'POST':
        data = request.get_json()
        if not data or 'name' not in data:
            return jsonify({'error': 'Name is required'}), 400
        
        cursor = db.execute(
            'INSERT INTO items (name, description) VALUES (?, ?)',
            (data['name'], data.get('description', ''))
        )
        db.commit()
        
        return jsonify({
            'id': cursor.lastrowid,
            'name': data['name'],
            'description': data.get('description', '')
        }), 201


@app.route('/items/<int:item_id>', methods=['GET', 'PUT', 'DELETE'])
def item(item_id):
    """Get, update or delete a specific item"""
    db = get_db()
    
    if request.method == 'GET':
        cursor = db.execute('SELECT * FROM items WHERE id = ?', (item_id,))
        item = cursor.fetchone()
        if item is None:
            return jsonify({'error': 'Item not found'}), 404
        return jsonify(dict(item))
    
    elif request.method == 'PUT':
        data = request.get_json()
        if not data or 'name' not in data:
            return jsonify({'error': 'Name is required'}), 400
        
        cursor = db.execute('SELECT * FROM items WHERE id = ?', (item_id,))
        if cursor.fetchone() is None:
            return jsonify({'error': 'Item not found'}), 404
        
        db.execute(
            'UPDATE items SET name = ?, description = ? WHERE id = ?',
            (data['name'], data.get('description', ''), item_id)
        )
        db.commit()
        
        return jsonify({'id': item_id, 'message': 'Item updated'})
    
    elif request.method == 'DELETE':
        cursor = db.execute('SELECT * FROM items WHERE id = ?', (item_id,))
        if cursor.fetchone() is None:
            return jsonify({'error': 'Item not found'}), 404
        
        db.execute('DELETE FROM items WHERE id = ?', (item_id,))
        db.commit()
        
        return jsonify({'message': 'Item deleted'}), 200


if __name__ == '__main__':
    # Ensure data directory exists
    os.makedirs(os.path.dirname(app.config['DATABASE']), exist_ok=True)
    # Initialize database
    init_db()
    # Run application
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
